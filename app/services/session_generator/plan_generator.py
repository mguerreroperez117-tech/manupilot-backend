from datetime import timedelta
from app.services.session_generator.week_plan import generate_week_plan
from app.db.models.plan import (
    TrainingPlan,
    PlanGoal,
    InitialAssessment,
    PeriodicTest,
    NutritionAdvice
)
from app.config.training_config import TRAINING_CONFIG
from app.services.session_generator.comments import generate_comments

# ============================================================
# GENERADOR DE NUTRICIÓN INTELIGENTE (PARAMETRIZADO)
# ============================================================

def generate_nutrition_advice(session, phase, race_date):
    cfg = TRAINING_CONFIG["nutrition"]

    name = session.get("name", "").lower()
    duration = session.get("duration_min", 0)
    intensity = session.get("intensity", "")
    month = race_date.month

    advice = NutritionAdvice(pre="", during="", post="")

    # -------------------------
    # 1. Entrenamiento en ayunas
    # -------------------------
    fasted_cfg = cfg["fasted_training"]
    if fasted_cfg["enabled"]:
        if (
            duration <= fasted_cfg["max_duration_min"]
            and intensity in fasted_cfg["allowed_intensities"]
            and not any(key in name for key in fasted_cfg["exclude_keywords"])
        ):
            advice.pre = "Sesión apta para ayunas: solo agua y café/té si lo deseas."

    # -------------------------
    # 2. Carga progresiva de hidratos
    # -------------------------
    carb_cfg = cfg["carb_loading"]
    if any(key in name for key in ["tempo", "interval", "long"]):
        advice.pre = carb_cfg.get(phase, carb_cfg["base"])

    # -------------------------
    # 3. Adaptación al calor
    # -------------------------
    heat_cfg = cfg["heat_adaptation"]
    if heat_cfg["enabled"]:
        if month in heat_cfg["months"] and duration <= heat_cfg["max_duration_min"]:
            advice.pre = heat_cfg["pre"]
            advice.during = heat_cfg["during"]
            advice.post = heat_cfg["post"]

    # -------------------------
    # 4. Nutrición DURANTE
    # -------------------------
    during_cfg = cfg["during_session"]
    if (
        duration >= during_cfg["min_duration_for_carbs"]
        or "long" in name
        or "trail" in name
    ):
        advice.during = during_cfg["carbs_per_hour"]

    # -------------------------
    # 5. Nutrición POST
    # -------------------------
    post_cfg = cfg["post_session"]
    if session.get("type") == "strength":
        advice.post = post_cfg["strength"]
    else:
        advice.post = post_cfg["default"]

    return advice


# ============================================================
# GENERADOR COMPLETO DEL PLAN
# ============================================================

def generate_full_plan(start_date, race_date, objective, availability, athlete_state, user_id=1):
    plan_weeks = []
    all_sessions = []

    athlete_state["plan_start_date"] = start_date
    current_date = start_date

    goal = PlanGoal(**objective)

    # ============================
    # GENERACIÓN SEMANA A SEMANA
    # ============================
    while current_date <= race_date:
        week_sessions = generate_week_plan(
            start_date=current_date,
            race_date=race_date,
            objective=objective,
            availability=availability,
            athlete_state=athlete_state
        )

        # Añadir nutrición y comentarios a cada sesión
        for s in week_sessions:
            # Fase: si la sesión la trae, la usamos; si no, base
            phase = getattr(s, "phase", "base")

            if not s.rest:
                s.nutrition = generate_nutrition_advice(
                    session=s.dict(),
                    phase=phase,
                    race_date=goal.target_date
                )

                # Comentarios inteligentes (editables desde TRAINING_CONFIG)
                s.comments = generate_comments(
                    session=s.dict(),
                    phase=phase,
                    athlete_state=athlete_state
                )

        plan_weeks.append({
            "week_start": current_date,
            "sessions": week_sessions
        })

        all_sessions.extend(week_sessions)
        current_date += timedelta(days=7)

    # ============================
    # PRUEBA INICIAL
    # ============================
    initial_assessment = InitialAssessment(
        required=True,
        completed=False,
        protocol="3k_time_trial" if goal.type in ["10k", "21k"] else "strength_basic"
    )

    # ============================
    # PRUEBAS PERIÓDICAS
    # ============================
    if goal.type in ["10k", "21k"]:
        periodic_tests = [
            PeriodicTest(
                interval_weeks=4,
                type="threshold_test",
                description="Test de umbral para recalibrar zonas"
            )
        ]
    elif goal.type == "trail":
        periodic_tests = [
            PeriodicTest(
                interval_weeks=5,
                type="trail_specific",
                description="Test de subida continua para evaluar fuerza y resistencia"
            )
        ]
    elif goal.type == "strength":
        periodic_tests = [
            PeriodicTest(
                interval_weeks=3,
                type="strength_test",
                description="Test de fuerza para ajustar cargas"
            )
        ]
    else:
        periodic_tests = []

    # ============================
    # CREACIÓN DEL PLAN FINAL
    # ============================
    training_plan = TrainingPlan(
        user_id=user_id,
        goal=goal,
        milestones=[],
        initial_assessment=initial_assessment,
        periodic_tests=periodic_tests,
        strength_focus=None,
        sessions=all_sessions
    )

    return training_plan
