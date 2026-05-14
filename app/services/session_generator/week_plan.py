from datetime import timedelta
from app.services.session_generator.generator import generate_daily_session
from app.config.training_config import TRAINING_CONFIG
from app.services.comments.comment_engine import generate_comments


# ============================================================
# FASE DEL PLAN
# ============================================================

def get_phase(current_week, total_weeks):
    base_end = int(total_weeks * 0.40)
    build_end = base_end + int(total_weeks * 0.35)
    peak_end = build_end + int(total_weeks * 0.15)

    if current_week < base_end:
        return "base"
    elif current_week < build_end:
        return "build"
    elif current_week < peak_end:
        return "peak"
    else:
        return "taper"


# ============================================================
# PROGRESIÓN DE VOLUMEN
# ============================================================

def compute_volume_progression(current_week, total_weeks):
    if current_week >= total_weeks - 2:
        return 0.6

    cycle = current_week % 4
    if cycle == 0:
        return 1.00
    elif cycle == 1:
        return 1.07
    elif cycle == 2:
        return 1.15
    else:
        return 0.70


# ============================================================
# PROGRESIÓN DE DESNIVEL PARA TRAIL
# ============================================================

def compute_trail_elevation_progression(current_week, total_weeks, athlete_level="intermediate"):
    base_dplus = {
        "beginner": 400,
        "intermediate": 1000,
        "advanced": 2000
    }.get(athlete_level, 1000)

    cycle = current_week % 4
    if cycle == 0:
        factor = 1.0
    elif cycle == 1:
        factor = 1.15
    elif cycle == 2:
        factor = 1.30
    else:
        factor = 0.70

    if current_week >= total_weeks - 2:
        factor = 0.50

    dplus = int(base_dplus * factor)
    dminus = int(dplus * (0.8 if factor >= 1 else 0.5))

    return dplus, dminus


# ============================================================
# ANÁLISIS 80/20
# ============================================================

def analyze_intensity_distribution(week_sessions):
    easy = 0
    quality = 0

    for s in week_sessions:
        if s.get("rest"):
            continue

        intensity = s.get("intensity")
        if not intensity:
            continue

        if intensity.startswith("Z"):
            z = int(intensity[1:])
            if z <= 2:
                easy += 1
            else:
                quality += 1

    return easy, quality


def adjust_80_20(week_sessions):
    easy, quality = analyze_intensity_distribution(week_sessions)
    total = easy + quality

    if total == 0:
        return week_sessions

    target_quality = max(1, int(total * 0.20))

    if quality > target_quality:
        excess = quality - target_quality
        for s in week_sessions:
            if excess == 0:
                break
            intensity = s.get("intensity")
            if intensity and intensity.startswith("Z"):
                z = int(intensity[1:])
                if z >= 3:
                    s["intensity"] = "Z2"
                    excess -= 1

    elif quality < target_quality:
        deficit = target_quality - quality
        for s in week_sessions:
            if deficit == 0:
                break
            if s.get("intensity") == "Z2":
                s["intensity"] = "Z3"
                deficit -= 1

    return week_sessions


# ============================================================
# SESIONES DE CALOR (BÁSICO)
# ============================================================

def apply_heat_session_logic(session, date, phase):
    cfg = TRAINING_CONFIG["nutrition"]["heat_adaptation"]

    if not cfg["enabled"]:
        return session

    if date.month not in cfg["months"]:
        return session

    if session.get("duration_min", 0) > cfg["max_duration_min"]:
        return session

    if phase not in ["base", "build"]:
        return session

    session["heat_session"] = True
    session["notes"] = "Sesión de adaptación al calor"

    return session


# ============================================================
# SESIONES DE AYUNO BÁSICO
# ============================================================

def apply_fasted_session_logic(session):
    cfg = TRAINING_CONFIG["nutrition"]["fasted_training"]

    if not cfg["enabled"]:
        return session

    if session.get("intensity") not in cfg["allowed_intensities"]:
        return session

    if session.get("duration_min", 0) > cfg["max_duration_min"]:
        return session

    name = session.get("name", "").lower()
    if any(key in name for key in cfg["exclude_keywords"]):
        return session

    session["fasted"] = True
    return session


# ============================================================
# SESIONES DE AYUNO AVANZADO POR FASE
# ============================================================

def apply_advanced_fasted_logic(session, phase):
    cfg = TRAINING_CONFIG["nutrition"]["advanced_fasted"]

    if not cfg["enabled"]:
        return session

    if phase not in cfg["phases"]:
        return session

    intensity = session.get("intensity")
    duration = session.get("duration_min", 0)
    name = session.get("name", "").lower()

    if intensity not in cfg["allowed_intensities"]:
        return session

    if duration > cfg["max_duration_min"]:
        return session

    if any(key in name for key in ["tempo", "interval", "long"]):
        return session

    session["fasted_advanced"] = True
    session["fasted_note"] = cfg["progression"].get(phase, "")

    return session


# ============================================================
# TÉCNICA PROGRESIVA POR FASE
# ============================================================

def apply_technique_progression(session, phase):
    if session.get("type") != "technique":
        return session

    cfg = TRAINING_CONFIG["training"]["technique_progression"]
    drills_cfg = TRAINING_CONFIG["training"]["technique_drills"]

    categories = cfg.get(phase, [])
    if not categories:
        return session

    drills = []
    for cat in categories:
        drills.extend(drills_cfg.get(cat, []))

    session["drills"] = drills
    return session


# ============================================================
# FUERZA PERIODIZADA POR FASE
# ============================================================

def apply_strength_periodization(session, phase):
    if session.get("type") != "strength":
        return session

    cfg = TRAINING_CONFIG["training"]["strength_periodization"]
    exercises_cfg = TRAINING_CONFIG["training"]["strength_exercises"]

    category = cfg.get(phase)
    if not category:
        return session

    exercises = exercises_cfg.get(category, [])
    session["exercises"] = exercises

    return session


# ============================================================
# COMPETICIONES INTERMEDIAS
# ============================================================

def get_intermediate_race_in_week(start_date, athlete_state):
    races = athlete_state.get("intermediate_races", [])
    week_end = start_date + timedelta(days=6)

    for race in races:
        race_date = race["date"]
        if start_date <= race_date <= week_end:
            return race

    return None


def apply_intermediate_race_logic(session, day, intermediate_race):
    if not intermediate_race:
        return session

    race_date = intermediate_race["date"]

    # Día de competición
    if day == race_date:
        session["is_race"] = True
        session["race_type"] = intermediate_race.get("type")
        session["race_priority"] = intermediate_race.get("priority", "B")
        session["name"] = f"Competición {session.get('race_type', '').upper()}"
        session["intensity"] = "race"
        session["race_goal_time_min"] = intermediate_race.get("goal_time_min")

    # Día anterior: descarga ligera
    elif day == race_date - timedelta(days=1):
        if session.get("type") == "run":
            session["taper_for_race"] = True
            session["intensity"] = "Z1"
            session["duration_min"] = min(session.get("duration_min", 40), 30)
            session["name"] = "Rodaje suave pre-competición"

    # Día posterior: recuperación
    elif day == race_date + timedelta(days=1):
        session["post_race_recovery"] = True
        session["type"] = "run"
        session["name"] = "Rodaje recuperación post-competición"
        session["intensity"] = "Z1"
        session["duration_min"] = 30

    return session


# ============================================================
# GENERADOR SEMANAL COMPLETO
# ============================================================

def generate_week_plan(start_date, race_date, objective, availability, athlete_state):
    total_weeks = max(1, (race_date - start_date).days // 7)
    current_week = max(0, (start_date - athlete_state.get("plan_start_date", start_date)).days // 7)

    phase = get_phase(current_week, total_weeks)
    volume_factor = compute_volume_progression(current_week, total_weeks)

    if objective.get("type") == "trail":
        dplus_target, dminus_target = compute_trail_elevation_progression(
            current_week, total_weeks, athlete_state.get("level", "intermediate")
        )
    else:
        dplus_target = dminus_target = 0

    intermediate_race = get_intermediate_race_in_week(start_date, athlete_state)

    week_sessions = []

    for i in range(7):
        day = start_date + timedelta(days=i)
        session = generate_daily_session(day, objective, phase, availability, athlete_state)

        # Ajuste de volumen
        if "duration_min" in session:
            session["duration_min"] = int(session["duration_min"] * volume_factor)

        # Calor
        session = apply_heat_session_logic(session, day, phase)

        # Ayuno básico
        session = apply_fasted_session_logic(session)

        # Ayuno avanzado
        session = apply_advanced_fasted_logic(session, phase)

        # Técnica progresiva
        session = apply_technique_progression(session, phase)

        # Fuerza periodizada
        session = apply_strength_periodization(session, phase)

        # Competición intermedia
        session = apply_intermediate_race_logic(session, day, intermediate_race)

        # Trail: desnivel
        if objective.get("type") == "trail" and session.get("type") == "run":
            subtype = session.get("subtype", "")
            if subtype == "long_run":
                session["dplus"] = int(dplus_target * 0.5)
                session["dminus"] = int(dminus_target * 0.5)
            elif subtype == "hill":
                session["dplus"] = int(dplus_target * 0.3)
                session["dminus"] = int(dminus_target * 0.3)
            else:
                session["dplus"] = int(dplus_target * 0.2)
                session["dminus"] = int(dminus_target * 0.2)

        # Comentarios inteligentes
        session = generate_comments(session, phase)

        week_sessions.append(session)

    # Ajuste 80/20
    week_sessions = adjust_80_20(week_sessions)

    return week_sessions
