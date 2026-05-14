from datetime import timedelta
from backend.app.database import get_connection
from backend.app.models.activity_db import Activity
from app.services.adaptive import (
    calculate_strength_impact,
    adaptive_factor_from_activity,
    adaptive_factor_from_state,
    combine_factors,
)
from app.config.training_config import TRAINING_CONFIG


# ============================================================
# UTILIDADES DE RITMO E INTENSIDAD
# ============================================================

def pace_to_seconds(pace_str):
    try:
        minutes, seconds = pace_str.replace("/km", "").split(":")
        return int(minutes) * 60 + int(seconds)
    except:
        return None


def seconds_to_pace(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02d}/km"


def adjust_pace(pace_str, factor):
    """Ajusta ritmo según factor adaptativo."""
    base_sec = pace_to_seconds(pace_str)
    if base_sec is None:
        return pace_str
    new_sec = int(base_sec / factor)
    return seconds_to_pace(new_sec)


def adjust_intensity(intensity, factor):
    """Reduce zona si el atleta está fatigado."""
    if not intensity or not intensity.startswith("Z"):
        return intensity

    if factor >= 0.85:
        return intensity

    try:
        z = int(intensity[1:])
        if z > 1:
            return f"Z{z-1}"
    except:
        pass

    return intensity


def adjust_elevation(elevation, factor):
    """Reduce desnivel si el atleta está fatigado."""
    if elevation <= 0:
        return elevation
    return int(elevation * factor)


# ============================================================
# ADAPTATIVO CONFIGURABLE POR PRS
# ============================================================

def compute_prs_factor(prs):
    """
    Devuelve un factor adaptativo según PRS usando TRAINING_CONFIG.
    """
    cfg = TRAINING_CONFIG["training"]["fatigue_adjustments"]

    if prs is None:
        return 1.0

    if prs >= 7:
        return cfg["low"]      # 1.0 por defecto
    if prs >= 5:
        return cfg["medium"]   # 0.95 por defecto
    return cfg["high"]         # 0.85 por defecto


def should_cancel_session(prs):
    """Cancela sesión si PRS es extremadamente bajo."""
    return prs is not None and prs < 3


# ============================================================
# ACTIVIDADES POR FECHA
# ============================================================

def get_activities_by_date():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, source, type, start_time, duration_sec, distance_m,
               elevation_gain_m, avg_hr, max_hr, rpe, tss, calories,
               notes, perceived_recovery
        FROM activities
    """)

    rows = cursor.fetchall()
    conn.close()

    activities = [Activity(**dict(r)) for r in rows]

    activities_by_date = {}
    for act in activities:
        d = act.start_time.date()
        if d not in activities_by_date:
            activities_by_date[d] = []
        activities_by_date[d].append(act)

    return activities_by_date


# ============================================================
# FUNCIÓN PRINCIPAL DEL ADAPTATIVO
# ============================================================

def apply_strength_corrections(plan):
    """
    Aplica TODA la lógica adaptativa:
    - impacto de fuerza del día anterior
    - impacto de actividad del día anterior
    - PRS del atleta
    - ajustes configurables desde training_config.py
    - cancelación de sesión
    - reducción de duración
    - reducción de intensidad
    - ajuste de ritmo
    - ajuste de desnivel
    """

    activities_by_date = get_activities_by_date()
    corrected_plan = []

    for session in plan:
        day = session["date"]
        prev_day = day - timedelta(days=1)

        prev_acts = activities_by_date.get(prev_day, [])

        # -------------------------
        # 1. Impacto de fuerza
        # -------------------------
        strength_sessions = [a for a in prev_acts if a.type == "strength"]
        strength = strength_sessions[0] if strength_sessions else None

        if strength:
            impact = calculate_strength_impact(strength)
            strength_factor = impact["factor_corrector"]
        else:
            strength_factor = 1.0

        # -------------------------
        # 2. Factor por actividad del día anterior
        # -------------------------
        activity_factor = adaptive_factor_from_activity(prev_acts)

        # -------------------------
        # 3. Factor por PRS (configurable)
        # -------------------------
        prs = strength.perceived_recovery if strength else None
        prs_factor = compute_prs_factor(prs)

        # -------------------------
        # 4. Factor por estado general (tu lógica actual)
        # -------------------------
        state_factor = adaptive_factor_from_state(
            prs=prs,
            sleep_quality=None,
            stress=None,
            soreness=None,
            motivation=None,
        )

        # -------------------------
        # 5. Factor final combinado
        # -------------------------
        final_factor = combine_factors(
            strength_factor,
            activity_factor,
            prs_factor,
            state_factor
        )

        print("FINAL FACTOR:", final_factor)

        # -------------------------
        # 6. Cancelación
        # -------------------------
        if should_cancel_session(prs):
            session["cancelled"] = True
            session["reason"] = "Fatiga extrema (PRS < 3)"
            corrected_plan.append(session)
            continue

        # -------------------------
        # 7. Ajuste de duración
        # -------------------------
        if "duration_min" in session:
            session["duration_min"] = int(session["duration_min"] * final_factor)

        # -------------------------
        # 8. Ajuste de intensidad
        # -------------------------
        if "intensity" in session:
            session["intensity"] = adjust_intensity(session["intensity"], final_factor)

        # -------------------------
        # 9. Ajuste de ritmo
        # -------------------------
        if "target_pace" in session and session["target_pace"]:
            session["target_pace"] = adjust_pace(session["target_pace"], final_factor)

        # -------------------------
        # 10. Ajuste de desnivel
        # -------------------------
        if "elevation" in session:
            session["elevation"] = adjust_elevation(session["elevation"], final_factor)

        corrected_plan.append(session)

    return corrected_plan
