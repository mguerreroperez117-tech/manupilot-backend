from fitparse import FitFile
from io import BytesIO
from datetime import datetime

def parse_fit_file(raw_bytes: bytes):
    fitfile = FitFile(BytesIO(raw_bytes))

    samples = {
        "time": [],
        "lat": [],
        "lon": [],
        "alt": [],
        "hr": [],
        "pace": [],
        "power": []
    }

    summary = {
        "duration_sec": 0,
        "distance_m": 0,
        "elevation_gain_m": 0,
        "elevation_loss_m": 0
    }

    device = {}
    start_time = None
    activity_type = "unknown"

    last_alt = None

    # ---------------------------------------------------------
    # 1. Leer mensajes de sesión (summary)
    # ---------------------------------------------------------
    for msg in fitfile.get_messages("session"):
        for field in msg:
            if field.name == "start_time":
                start_time = field.value
            if field.name == "sport":
                activity_type = field.value
            if field.name == "total_elapsed_time":
                summary["duration_sec"] = field.value
            if field.name == "total_distance":
                summary["distance_m"] = field.value

    # ---------------------------------------------------------
    # 2. Leer device info
    # ---------------------------------------------------------
    for msg in fitfile.get_messages("device_info"):
        for field in msg:
            if field.name == "manufacturer":
                device["brand"] = field.value
            if field.name == "product_name":
                device["model"] = field.value
            if field.name == "software_version":
                device["firmware"] = str(field.value)

    # ---------------------------------------------------------
    # 3. Leer muestras (record)
    # ---------------------------------------------------------
    for record in fitfile.get_messages("record"):
        fields = {f.name: f.value for f in record}

        # Tiempo
        ts = fields.get("timestamp")
        samples["time"].append(ts.isoformat() if ts else None)

        # Lat/Lon
        if "position_lat" in fields:
            samples["lat"].append(fields["position_lat"] * (180 / 2**31))
        else:
            samples["lat"].append(None)

        if "position_long" in fields:
            samples["lon"].append(fields["position_long"] * (180 / 2**31))
        else:
            samples["lon"].append(None)

        # Altitud
        alt = fields.get("altitude")
        samples["alt"].append(float(alt) if alt else None)

        # HR
        samples["hr"].append(fields.get("heart_rate"))

        # Power
        samples["power"].append(fields.get("power"))

        # Pace (si hay velocidad)
        speed = fields.get("speed")
        samples["pace"].append(1000 / speed if speed and speed > 0 else None)

        # Desnivel
        if alt is not None:
            if last_alt is not None:
                diff = alt - last_alt
                if diff > 0:
                    summary["elevation_gain_m"] += diff
                else:
                    summary["elevation_loss_m"] += abs(diff)
            last_alt = alt

    return {
        "summary": summary,
        "samples": samples,
        "device": device,
        "start_time": start_time,
        "type": activity_type
    }

