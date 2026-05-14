from datetime import date, timedelta
from fastapi import APIRouter, Query
from app.services.session_generator.plan_generator import generate_full_plan

router = APIRouter(prefix="/plan", tags=["plan"])


# ============================================================
# PLAN COMPLETO
# ============================================================

@router.post("/")
def get_plan(payload: dict):
    start_date = date.fromisoformat(payload["start_date"])
    race_date = date.fromisoformat(payload["race_date"])

    plan = generate_full_plan(
        start_date=start_date,
        race_date=race_date,
        objective=payload["objective"],
        availability=payload["availability"],
        athlete_state=payload.get("athlete_state", {})
    )

    return {
        "start_date": start_date,
        "race_date": race_date,
        "weeks": plan
    }


# ============================================================
# DÍA CONCRETO
# ============================================================

@router.post("/day")
def get_day(date_str: str, payload: dict):
    target_date = date.fromisoformat(date_str)

    plan = generate_full_plan(
        start_date=target_date,
        race_date=date.fromisoformat(payload["race_date"]),
        objective=payload["objective"],
        availability=payload["availability"],
        athlete_state=payload.get("athlete_state", {})
    )

    for week in plan:
        for session in week["sessions"]:
            if session["date"] == target_date:
                return session

    return {"error": "No session found for this date"}


# ============================================================
# SEMANA COMPLETA
# ============================================================

@router.post("/week")
def get_week(start: str, payload: dict):
    start_date = date.fromisoformat(start)

    plan = generate_full_plan(
        start_date=start_date,
        race_date=date.fromisoformat(payload["race_date"]),
        objective=payload["objective"],
        availability=payload["availability"],
        athlete_state=payload.get("athlete_state", {})
    )

    return plan[0]


# ============================================================
# MES COMPLETO
# ============================================================

@router.post("/month")
def get_month(year: int, month: int, payload: dict):
    start_date = date(year, month, 1)

    plan = generate_full_plan(
        start_date=start_date,
        race_date=date.fromisoformat(payload["race_date"]),
        objective=payload["objective"],
        availability=payload["availability"],
        athlete_state=payload.get("athlete_state", {})
    )

    month_sessions = []
    for week in plan:
        for session in week["sessions"]:
            if session["date"].year == year and session["date"].month == month:
                month_sessions.append(session)

    return month_sessions


# ============================================================
# MÉTRICAS DEL PLAN
# ============================================================

@router.post("/metrics")
def get_metrics(payload: dict):
    start_date = date.fromisoformat(payload["start_date"])
    race_date = date.fromisoformat(payload["race_date"])

    plan = generate_full_plan(
        start_date=start_date,
        race_date=race_date,
        objective=payload["objective"],
        availability=payload["availability"],
        athlete_state=payload.get("athlete_state", {})
    )

    metrics = {
        "weekly": [],
        "total_volume_min": 0,
        "total_dplus": 0,
        "total_dminus": 0,
        "total_sessions": 0,
        "total_quality_sessions": 0
    }

    for week in plan:
        week_volume = 0
        week_dplus = 0
        week_dminus = 0
        week_quality = 0

        for s in week["sessions"]:
            if s.get("rest"):
                continue

            metrics["total_sessions"] += 1

            dur = s.get("duration_min", 0)
            week_volume += dur
            metrics["total_volume_min"] += dur

            dp = s.get("dplus", 0)
            dm = s.get("dminus", 0)
            week_dplus += dp
            week_dminus += dm
            metrics["total_dplus"] += dp
            metrics["total_dminus"] += dm

            intensity = s.get("intensity")
            if intensity and intensity.startswith("Z") and int(intensity[1:]) >= 3:
                week_quality += 1
                metrics["total_quality_sessions"] += 1

        metrics["weekly"].append({
            "week_start": week["week_start"],
            "volume_min": week_volume,
            "dplus": week_dplus,
            "dminus": week_dminus,
            "quality_sessions": week_quality
        })

    return metrics

