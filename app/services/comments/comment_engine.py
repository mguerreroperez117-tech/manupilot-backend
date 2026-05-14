from app.config.training_config import TRAINING_CONFIG


def generate_comments(session, phase):
    comments = []

    # ============================================================
    # 1. Comentarios por tipo de sesión
    # ============================================================
    type_comment = TRAINING_CONFIG["comments"]["types"].get(session.get("type"))
    if type_comment:
        comments.append(type_comment)

    # ============================================================
    # 2. Comentarios por fase del plan
    # ============================================================
    phase_comment = TRAINING_CONFIG["comments"]["phases"].get(phase)
    if phase_comment:
        comments.append(phase_comment)

    # ============================================================
    # 3. Comentarios especiales (calor, ayuno, trail, PRS)
    # ============================================================
    special_cfg = TRAINING_CONFIG["comments"]["special"]

    if session.get("heat_session"):
        comments.append(special_cfg["heat"])

    if session.get("fasted"):
        comments.append(special_cfg["fasted"])

    if session.get("fasted_advanced"):
        comments.append(session.get("fasted_note", ""))

    if session.get("dplus", 0) > 400:
        comments.append(special_cfg["trail_elevation"])

    if session.get("prs_low"):
        comments.append(special_cfg["prs_low"])

    if session.get("prs_high"):
        comments.append(special_cfg["prs_high"])

    # ============================================================
    # 4. Comentarios para competiciones intermedias
    # ============================================================

    # Día de carrera
    if session.get("is_race"):
        race_type = session.get("race_type", "").upper()
        comments.append(f"Hoy compites ({race_type}). Calienta bien y controla los primeros kilómetros.")

        # Estrategia general por tipo de carrera
        if race_type == "10K":
            comments.append("Estrategia: empieza controlado 2–3 km y progresa hasta Z4.")
        elif race_type == "21K":
            comments.append("Estrategia: mantén Z3 estable y aprieta del km 15 al 18.")
        elif race_type == "TRAIL":
            comments.append("Estrategia: en subidas 2' fuerte / 6' control, en bajadas técnica fluida.")

    # Día previo
    if session.get("taper_for_race"):
        comments.append("Mañana compites: hoy solo activación suave y buena hidratación.")

    # Día posterior
    if session.get("post_race_recovery"):
        comments.append("Recuperación post-competición: mantén el ritmo muy suave y prioriza descanso.")

    # ============================================================
    # 5. Comentarios para fuerza periodizada
    # ============================================================

    if session.get("type") == "strength":
        exercises = session.get("exercises", [])

        if any("excéntrica" in e.get("type", "") for e in exercises):
            comments.append("Fuerza excéntrica: controla la bajada 3–4 segundos.")

        if any("potencia" in e.get("type", "") for e in exercises):
            comments.append("Fuerza de potencia: prioriza calidad, no volumen.")

        if any("general" in e.get("type", "") for e in exercises):
            comments.append("Fuerza general: céntrate en técnica y control del movimiento.")

    # ============================================================
    # 6. Comentarios para técnica progresiva
    # ============================================================

    if session.get("type") == "technique":
        comments.append("Concéntrate en postura, cadencia y relajación de hombros.")
        comments.append("Busca fluidez, no velocidad.")

    # ============================================================
    # 7. Comentarios para trail según subtipo
    # ============================================================

    subtype = session.get("subtype")

    if subtype == "long_run":
        comments.append("Tirada larga trail: mantén ritmo constante y bebe cada 20–25 min.")

    if subtype == "hill":
        comments.append("Cuestas: empuja fuerte en la subida y recupera caminando si es necesario.")

    # ============================================================
    # 8. Comentarios finales
    # ============================================================

    session["comments"] = comments
    return session

