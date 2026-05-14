from datetime import datetime

# ----------------------------------------
# Obtener actividades (placeholder)
# ----------------------------------------
def get_activities():
    # TODO: conectar a PostgreSQL con SQLAlchemy
    # De momento devolvemos lista vacía para no romper el servidor
    return []

# ----------------------------------------
# Constantes de TrainingPeaks
# ----------------------------------------
def calculate_load_constants():
    ATL_DAYS = 7
    CTL_DAYS = 42

    ATL_K = 2 / (ATL_DAYS + 1)
    CTL_K = 2 / (CTL_DAYS + 1)

    return ATL_K, CTL_K

# ----------------------------------------
# Cálculo CTL / ATL / TSB
# ----------------------------------------
def calculate_training_load():
    activities = get_activities()
    if not activities:
        return {"CTL": 0, "ATL": 0, "TSB": 0}

    ATL_K, CTL_K = calculate_load_constants()

    ctl = 0
    atl = 0
    last_date = None

    for act in activities:
        tss = act["tss"] or 0
        date = datetime.fromisoformat(act["start_time"])

        if last_date:
            days = (date - last_date).days
            for _ in range(days):
                ctl = ctl * (1 - CTL_K)
                atl = atl * (1 - ATL_K)

        ctl = ctl + CTL_K * (tss - ctl)
        atl = atl + ATL_K * (tss - atl)

        last_date = date

    tsb = ctl - atl

    return {
        "CTL": round(ctl, 2),
        "ATL": round(atl, 2),
        "TSB": round(tsb, 2)
    }

# ----------------------------------------
# Distribución por zonas (simple)
# ----------------------------------------
def calculate_zones_distribution():
    activities = get_activities()

    zones = {"Z1": 0, "Z2": 0, "Z3": 0, "Z4": 0, "Z5": 0}

    for act in activities:
        hr = act["avg_hr"]
        if not hr:
            continue

        if hr < 120:
            zones["Z1"] += 1
        elif hr < 140:
            zones["Z2"] += 1
        elif hr < 160:
            zones["Z3"] += 1
        elif hr < 175:
            zones["Z4"] += 1
        else:
            zones["Z5"] += 1

    return zones
