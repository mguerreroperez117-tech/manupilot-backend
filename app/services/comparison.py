def compare_plan_vs_real(planned, actual):
    result = {}

    # --- DURACIÓN ---
    planned_sec = planned.get("duration_min", 0) * 60
    real_sec = actual.get("duration_sec", 0)

    if planned_sec > 0:
        duration_pct = (real_sec - planned_sec) / planned_sec * 100
    else:
        duration_pct = 0

    result["duration_pct"] = round(duration_pct, 1)

    # --- INTENSIDAD ---
    planned_zone = planned.get("intensity", "Z2")
    real_hr = actual.get("avg_hr")

    if real_hr:
        # Zonas aproximadas (puedes ajustar)
        if real_hr < 140:
            real_zone = "Z1"
        elif real_hr < 150:
            real_zone = "Z2"
        elif real_hr < 160:
            real_zone = "Z3"
        elif real_hr < 170:
            real_zone = "Z4"
        else:
            real_zone = "Z5"
    else:
        real_zone = None

    if real_zone:
        planned_z = int(planned_zone[1:])
        real_z = int(real_zone[1:])
        shift = real_z - planned_z
        result["intensity_shift"] = shift
    else:
        result["intensity_shift"] = None

    # --- VOLUMEN (DISTANCIA) ---
    planned_dist = planned.get("distance_m", None)
    real_dist = actual.get("distance_m", None)

    if planned_dist and real_dist:
        result["volume_pct"] = round((real_dist - planned_dist) / planned_dist * 100, 1)
    else:
        result["volume_pct"] = None

    # --- DESNIVEL ---
    planned_dplus = planned.get("dplus", 0)
    real_dplus = actual.get("elevation_gain_m", 0)

    if planned_dplus > 0:
        result["dplus_pct"] = round((real_dplus - planned_dplus) / planned_dplus * 100, 1)
    else:
        result["dplus_pct"] = None

    # --- CARGA (simple TRIMP) ---
    if real_hr and real_sec:
        result["load_score"] = int((real_hr / 100) * (real_sec / 60))
    else:
        result["load_score"] = None

    # --- ESTADO ---
    result["status"] = "completed" if real_sec > 0 else "skipped"

    return result
