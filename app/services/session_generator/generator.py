from datetime import timedelta
from app.services.session_generator.templates import TEMPLATES
from app.db.models.plan import PlanSession
from app.config.training_config import TRAINING_CONFIG



# ============================================================
# UTILIDADES DE RITMOS Y ZONAS
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


def adjust_pace_for_fatigue(base_pace_sec, prs):
    cfg = TRAINING_CONFIG["training"]["fatigue_adjustments"]

    if prs < 5:
        factor = cfg["high"]
    elif prs < 7:
        factor = cfg["medium"]
    else:
        factor = cfg["low"]

    return int(base_pace_sec / factor)


def adjust_zone_for_fatigue(zone, prs):
    """Reduce la zona si el PRS es bajo."""
    if not zone.startswith("Z"):
        return zone

    z = int(zone[1:])

    if prs < 4:
        return f"Z{max(1, z-2)}"
    if prs < 6:
        return f"Z{max(1, z-1)}"

    return zone


# ============================================================
# PATRONES SEMANALES
# ============================================================

WEEK_PATTERN_10K = {
    "monday": "strength_general",
    "tuesday": "tempo",
    "wednesday": "easy",
    "thursday": "intervals",
    "friday": "easy",
    "saturday": "long_run",
    "sunday": None
}

WEEK_PATTERN_21K = WEEK_PATTERN_10K.copy()

WEEK_PATTERN_TRAIL = {
    "monday": "strength_excentric",
    "tuesday": "easy_trail",
    "wednesday": "hike_run",
    "thursday": "hill_repeats",
    "friday": "easy_trail",
    "saturday": "long_run_trail",
    "sunday": None
}


def _get_week_pattern(objective_type: str):
    objective_type = objective_type.lower()
    if objective_type == "10k":
        return WEEK_PATTERN_10K
    if objective_type == "21k":
        return WEEK_PATTERN_21K
    if objective_type == "trail":
        return WEEK_PATTERN_TRAIL
    return WEEK_PATTERN_10K


# ============================================================
# ELECCIÓN DE PLANTILLA
# ============================================================

def choose_template(objective: dict, phase: str, day_name: str):
    objective_type = objective.get("type", "10k").lower()
    phase = phase.lower()
    day_name = day_name.lower()

    week_pattern = _get_week_pattern(objective_type)
    session_key = week_pattern.get(day_name)

    if session_key is None:
        return None

    objective_block = TEMPLATES.get(objective_type, {})
    phase_block = objective_block.get(phase, {})

    template = phase_block.get(session_key)

    if template is None and phase != "base":
        template = objective_block.get("base", {}).get(session_key)

    if template is None:
        template = phase_block.get("easy") or phase_block.get("easy_trail")

    return template


# ============================================================
# DURACIÓN SEGÚN DISPONIBILIDAD
# ============================================================

def choose_duration(time_slot):
    if time_slot == "short":
        return 30
    if time_slot == "medium":
        return 45
    if time_slot == "long":
        return 75
    return 45


# ============================================================
# ESTRATEGIAS DE CARRERA
# ============================================================

def apply_race_strategy(session, objective_type):
    """Añade pacing y bloques según tipo de carrera."""
    if not session.get("is_race"):
        return session

    if objective_type == "10k":
        # Estrategia A: progresivo Z2 → Z3 → Z4
        session["blocks"] = [
            {"duration_min": 10, "intensity": "Z2"},
            {"duration_min": 15, "intensity": "Z3"},
            {"duration_min": 15, "intensity": "Z4"},
        ]
        session["strategy"] = "Progresivo: empieza suave y acaba fuerte."

    elif objective_type == "21k":
        # Estrategia A: steady Z3
        session["blocks"] = [
            {"duration_min": session["duration_min"], "intensity": "Z3"}
        ]
        session["strategy"] = "Ritmo estable en Z3 durante toda la carrera."

    elif objective_type == "trail":
        # Estrategia B: subidas Z3, bajadas técnica
        session["strategy"] = "Subidas Z3, bajadas técnica fluida."
        session["notes"] = "En subidas: empuja fuerte. En bajadas: controla técnica."

    return session


# ============================================================
# INTERVALOS ADAPTATIVOS
# ============================================================

def adapt_intervals(session, duration, prs):
    if "intervals" not in session:
        return session

    base_reps = session.get("reps", 1)
    work = session["intervals"][0]["work"]["duration_min"]
    rest = session["intervals"][0]["rest"]["duration_min"]

    total_interval_time = (work + rest) * base_reps

    if total_interval_time > duration:
        factor = duration / total_interval_time
        new_reps = max(1, int(base_reps * factor))
        session["reps"] = new_reps

    # Ajuste por PRS
    if prs < 5:
        session["intervals"][0]["work"]["intensity"] = "Z3"

    return session


# ============================================================
# BLOQUES DINÁMICOS
# ============================================================

def adapt_blocks(session, duration, prs):
    if "blocks" not in session:
        return session

    total = sum(b["duration_min"] for b in session["blocks"])
    if total == 0:
        return session

    factor = duration / total

    for block in session["blocks"]:
        block["duration_min"] = int(block["duration_min"] * factor)

        # Ajuste por PRS
        block["intensity"] = adjust_zone_for_fatigue(block["intensity"], prs)

    return session


# ============================================================
# CONSTRUCTOR AVANZADO DE SESIONES
# ============================================================

def build_session_from_template(template, duration, availability, day_name, objective, phase, athlete_state):
    if template is None:
        return {"type": "rest", "description": "Descanso según patrón semanal"}

    session = {
        "name": template.get("name"),
        "type": template.get("type", "run"),
    }

    prs = athlete_state.get("prs", 7)
    objective_type = objective.get("type", "10k")

    # -------------------------
    # 1. Duración
    # -------------------------
    if "duration_range" in template:
        min_dur, max_dur = template["duration_range"]
        if duration <= 35:
            session["duration_min"] = min_dur
        elif duration <= 60:
            session["duration_min"] = (min_dur + max_dur) // 2
        else:
            session["duration_min"] = max_dur
    else:
        session["duration_min"] = duration

    # -------------------------
    # 2. Intensidad base
    # -------------------------
    zone = template.get("intensity", "Z2")
    zone = adjust_zone_for_fatigue(zone, prs)
    session["intensity"] = zone

    # -------------------------
    # 3. Ritmo objetivo
    # -------------------------
    paces_cfg = TRAINING_CONFIG["training"]["paces"]
    base_pace_str = paces_cfg.get(zone, paces_cfg["Z2"])
    base_pace_sec = pace_to_seconds(base_pace_str)
    adjusted_pace_sec = adjust_pace_for_fatigue(base_pace_sec, prs)
    session["target_pace"] = seconds_to_pace(adjusted_pace_sec)

    # -------------------------
    # 4. Bloques
    # -------------------------
    if "blocks" in template:
        session["blocks"] = [b.copy() for b in template["blocks"]]
        session = adapt_blocks(session, session["duration_min"], prs)

    # -------------------------
    # 5. Intervalos
    # -------------------------
    if "intervals" in template:
        session["intervals"] = template["intervals"]
        session["reps"] = template.get("reps", 1)
        session = adapt_intervals(session, session["duration_min"], prs)

    # -------------------------
    # 6. Terreno y desnivel
    # -------------------------
    if "terrain" in template:
        session["terrain"] = template["terrain"]

    if "elevation" in template:
        session["elevation"] = template["elevation"]

    # -------------------------
    # 7. Fuerza / Técnica
    # -------------------------
    if template.get("type") == "strength":
        session["exercises"] = template.get("exercises", [])

    if template.get("type") == "technique":
        session["drills"] = template.get("drills", [])

    # -------------------------
    # 8. Estrategia de carrera
    # -------------------------
    session = apply_race_strategy(session, objective_type)

    return session


# ============================================================
# ADAPTATIVO FINAL
# ============================================================

def compute_adaptive_factor(athlete_state):
    prs = athlete_state.get("prs", 10)
    cfg = TRAINING_CONFIG["training"]["fatigue_adjustments"]

    if prs >= 7:
        return cfg["low"]
    if prs >= 5:
        return cfg["medium"]
    return cfg["high"]


def adjust_session(session, final_factor):
    if session.get("type") == "rest":
        return session

    if "duration_min" in session:
        session["duration_min"] = int(session["duration_min"] * final_factor)

    intensity = session.get("intensity")
    if intensity and intensity.startswith("Z") and final_factor < 0.75:
        try:
            z = int(intensity[1:])
            if z > 1:
                session["intensity"] = f"Z{z-1}"
        except:
            pass

    if final_factor < 0.55:
        session["cancelled"] = True

    return session


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def generate_daily_session(date, objective, phase, availability, athlete_state):
    day_name = date.strftime("%A").lower()

    if availability["daily_time"].get(day_name) == "rest":
        return PlanSession(
            date=date,
            name="Descanso",
            type="rest",
            rest=True
        )

    duration = choose_duration(availability["daily_time"][day_name])
    base_template = choose_template(objective, phase, day_name)

    session = build_session_from_template(
        base_template,
        duration,
        availability,
        day_name,
        objective,
        phase,
        athlete_state
    )

    final_factor = compute_adaptive_factor(athlete_state)
    session = adjust_session(session, final_factor)

    session["date"] = date

    return PlanSession(**session)

