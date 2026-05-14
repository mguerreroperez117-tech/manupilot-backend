from dataclasses import dataclass
from backend.app.models.activity_db import Activity

@dataclass
class StrengthImpact:
    nm: float
    nm_final: float
    factor_corrector: float

def get_type_factor(activity: Activity) -> float:
    notes = (activity.notes or "").lower()

    if "core" in notes or "movilidad" in notes:
        return 0.3
    if "general" in notes:
        return 0.6
    if "pierna moderada" in notes:
        return 1.0
    if "pierna pesada" in notes:
        return 1.3
    if "excéntrico" in notes or "maxima" in notes:
        return 1.5

    return 0.8  # por defecto

def get_prs_factor(perceived_recovery: int | None) -> float:
    if perceived_recovery is None:
        return 1.0
    if perceived_recovery <= 2:
        return 1.4
    if perceived_recovery <= 4:
        return 1.2
    if perceived_recovery <= 6:
        return 1.0
    if perceived_recovery <= 8:
        return 0.85
    return 0.7

def calculate_strength_impact(activity: Activity) -> StrengthImpact:
    if activity.type != "strength":
        return StrengthImpact(nm=0.0, nm_final=0.0, factor_corrector=1.0)

    duration_min = activity.duration_sec / 60
    rpe = activity.rpe or 5
    type_factor = get_type_factor(activity)
    prs_factor = get_prs_factor(activity.perceived_recovery)

    nm = (rpe / 10) * (duration_min / 60) * type_factor
    nm_final = nm * prs_factor
    factor_corrector = max(0.5, 1 - (nm_final * 0.3))

    return StrengthImpact(
        nm=round(nm, 3),
        nm_final=round(nm_final, 3),
        factor_corrector=round(factor_corrector, 3),
    )
