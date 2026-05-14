# app/services/adaptive.py

from typing import Optional
from backend.app.database import get_config_value


# -----------------------------
# Helpers
# -----------------------------

def _safe(value: Optional[float | int], default: float = 0.0) -> float:
    return float(value) if value is not None else default


# -----------------------------
# FACTOR POR SESIÓN DEL DÍA ANTERIOR
# -----------------------------

def adaptive_factor_from_activity(
    *,
    planned_duration_min: Optional[float] = None,
    actual_duration_min: Optional[float] = None,
    tss: Optional[float] = None,
    rpe: Optional[int] = None,
    cardiac_drift_pct: Optional[float] = None,
    hr_max_pct: Optional[float] = None,
) -> float:
    """
    Devuelve un factor corrector (0–1) basado en cómo fue la sesión del día anterior.
    Cuanto más dura/estresante, más bajo el factor.
    """

    factors: list[float] = []

    # -----------------------------
    # TSS
    # -----------------------------
    tss_val = _safe(tss)

    tss_high_th = get_config_value("tss_high_threshold", 110)
    tss_very_high_th = get_config_value("tss_very_high_threshold", 140)

    tss_high_factor = get_config_value("tss_high_factor", 0.7)
    tss_very_high_factor = get_config_value("tss_very_high_factor", 0.6)

    if tss_val > tss_very_high_th:
        factors.append(tss_very_high_factor)
    elif tss_val > tss_high_th:
        factors.append(tss_high_factor)
    elif tss_val > 90:
        factors.append(0.8)  # valor base si no está configurado

    # -----------------------------
    # RPE
    # -----------------------------
    rpe_val = _safe(rpe)

    if rpe_val >= 9:
        factors.append(0.7)
    elif rpe_val >= 8:
        factors.append(0.8)
    elif rpe_val >= 7:
        factors.append(0.9)

    # -----------------------------
    # Duración real vs planificada
    # -----------------------------
    if planned_duration_min is not None and actual_duration_min is not None:
        planned = _safe(planned_duration_min, 1.0)
        actual = _safe(actual_duration_min)
        if planned > 0:
            ratio = actual / planned
            if ratio >= 1.4:
                factors.append(0.7)
            elif ratio >= 1.2:
                factors.append(0.85)

    # -----------------------------
    # Deriva cardíaca
    # -----------------------------
    drift = _safe(cardiac_drift_pct)
    if drift >= 8:
        factors.append(0.75)
    elif drift >= 5:
        factors.append(0.85)

    # -----------------------------
    # HR máx relativa
    # -----------------------------
    hr_max_rel = _safe(hr_max_pct)
    if hr_max_rel >= 98:
        factors.append(0.8)
    elif hr_max_rel >= 95:
        factors.append(0.9)

    if not factors:
        return 1.0

    min_factor = get_config_value("min_factor", 0.4)
    return max(min_factor, min(factors))


# -----------------------------
# FACTOR POR ESTADO SUBJETIVO (PRS, ETC.)
# -----------------------------

def adaptive_factor_from_state(
    *,
    prs: Optional[int] = None,
    sleep_quality: Optional[int] = None,
    stress: Optional[int] = None,
    soreness: Optional[int] = None,
    motivation: Optional[int] = None,
) -> float:
    """
    Devuelve un factor corrector (0–1) basado en el estado percibido del atleta.
    """

    factors: list[float] = []

    # -----------------------------
    # PRS
    # -----------------------------
    prs_val = _safe(prs)

    prs_low_factor = get_config_value("prs_low_factor", 0.6)
    prs_medium_factor = get_config_value("prs_medium_factor", 0.75)

    if prs_val <= 3:
        factors.append(prs_low_factor)
    elif prs_val <= 5:
        factors.append(prs_medium_factor)
    elif prs_val <= 7:
        factors.append(0.9)
    else:
        factors.append(1.0)

    # -----------------------------
    # Sueño
    # -----------------------------
    sleep_val = _safe(sleep_quality)
    if sleep_val and sleep_val <= 4:
        factors.append(0.7)
    elif sleep_val and sleep_val <= 6:
        factors.append(0.85)

    # -----------------------------
    # Estrés
    # -----------------------------
    stress_val = _safe(stress)
    if stress_val >= 8:
        factors.append(0.7)
    elif stress_val >= 6:
        factors.append(0.85)

    # -----------------------------
    # Dolor muscular
    # -----------------------------
    soreness_val = _safe(soreness)
    if soreness_val >= 8:
        factors.append(0.6)
    elif soreness_val >= 6:
        factors.append(0.8)

    # -----------------------------
    # Motivación
    # -----------------------------
    motivation_val = _safe(motivation)
    if motivation_val and motivation_val <= 3:
        factors.append(0.75)

    if not factors:
        return 1.0

    min_factor = get_config_value("min_factor", 0.4)
    return max(min_factor, min(factors))


# -----------------------------
# COMBINACIÓN DE FACTORES
# -----------------------------

def combine_factors(
    *,
    strength_factor: Optional[float] = None,
    activity_factor: Optional[float] = None,
    state_factor: Optional[float] = None,
) -> float:
    """
    Combina los factores de fuerza, sesión previa y estado subjetivo.
    Toma el más restrictivo (mínimo) y lo acota a [min_factor, 1.0].
    """

    factors = [
        f for f in [strength_factor, activity_factor, state_factor]
        if f is not None
    ]

    if not factors:
        return 1.0

    min_factor = get_config_value("min_factor", 0.3)
    return max(min_factor, min(factors))

