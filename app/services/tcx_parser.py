import xml.etree.ElementTree as ET
from datetime import datetime

def parse_tcx_file(content: bytes):
    root = ET.fromstring(content)

    ns = {
        "tcx": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
        "ns3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2"
    }

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

    start_time = None
    activity_type = "unknown"

    # Tipo de actividad
    activity = root.find(".//tcx:Activity", ns)
    if activity is not None:
        activity_type = activity.get("Sport", "unknown")

    last_alt = None
    last_dist = 0

    # Trackpoints
    for tp in root.findall(".//tcx:Trackpoint", ns):

        # Tiempo
        time_el = tp.find("tcx:Time", ns)
        if time_el is not None:
            t = datetime.fromisoformat(time_el.text.replace("Z", "+00:00"))
            samples["time"].append(t.isoformat())
            if start_time is None:
                start_time = t
            summary["duration_sec"] = (t - start_time).total_seconds()
        else:
            samples["time"].append(None)

        # Posición
        pos = tp.find("tcx:Position", ns)
        if pos is not None:
            lat_el = pos.find("tcx:LatitudeDegrees", ns)
            lon_el = pos.find("tcx:LongitudeDegrees", ns)
            samples["lat"].append(float(lat_el.text) if lat_el is not None else None)
            samples["lon"].append(float(lon_el.text) if lon_el is not None else None)
        else:
            samples["lat"].append(None)
            samples["lon"].append(None)

        # Altitud
        alt_el = tp.find("tcx:AltitudeMeters", ns)
        alt = float(alt_el.text) if alt_el is not None else None
        samples["alt"].append(alt)

        # Desnivel
        if alt is not None:
            if last_alt is not None:
                diff = alt - last_alt
                if diff > 0:
                    summary["elevation_gain_m"] += diff
                else:
                    summary["elevation_loss_m"] += abs(diff)
            last_alt = alt

        # HR
        hr_el = tp.find("tcx:HeartRateBpm/tcx:Value", ns)
        samples["hr"].append(int(hr_el.text) if hr_el is not None else None)

        # Distancia
        dist_el = tp.find("tcx:DistanceMeters", ns)
        if dist_el is not None:
            dist = float(dist_el.text)
            if dist > last_dist:
                summary["distance_m"] = dist
                last_dist = dist

        # Power
        power = None
        ext = tp.find("tcx:Extensions", ns)
        if ext is not None:
            watts = ext.find(".//ns3:Watts", ns)
            if watts is not None:
                power = int(watts.text)
        samples["power"].append(power)

        # Pace
        speed_el = tp.find(".//ns3:Speed", ns)
        if speed_el is not None:
            speed = float(speed_el.text)
            samples["pace"].append(1000 / speed if speed > 0 else None)
        else:
            samples["pace"].append(None)

    return {
        "summary": summary,
        "samples": samples,
        "device": {},
        "start_time": start_time,
        "type": activity_type
    }
