from app.config.training_config import TRAINING_CONFIG


def generate_comments(session: dict, phase: str, athlete_state: dict) -> str:
    cfg = TRAINING_CONFIG.get("comments", {})
    types_cfg = cfg.get("types", {})
    phases_cfg = cfg.get("phases", {})
    special_cfg = cfg.get("special", {})

    comments = []

    # -------------------------
    # 1. Comentario por tipo de sesión
    # -------------------------
    stype = session.get("type")
    if stype in types_cfg:
        comments.append(types_cfg[stype])

    # -------------------------
    # 2. Comentario por fase
    # -------------------------
    if phase in phases_cfg:
        comments.append(phases_cfg[phase])

    # -------------------------
    # 3. Comentarios especiales
    # -------------------------
    if session.get("heat_session") and "heat" in special_cfg:
        comments.append(special_cfg["heat"])

    if session.get("fasted") and "fasted" in special_cfg:
        comments.append(special_cfg["fasted"])

    if session.get("elevation", 0) > 0 and "trail_elevation" in special_cfg:
        comments.append(special_cfg["trail_elevation"])

    prs = athlete_state.get("prs")
    if prs is not None:
        if prs >= 8 and "prs_high" in special_cfg:
            comments.append(special_cfg["prs_high"])
        elif prs <= 4 and "prs_low" in special_cfg:
            comments.append(special_cfg["prs_low"])

    return " ".join(comments)
