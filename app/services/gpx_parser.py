import gpxpy

def parse_gpx_file(content: bytes):
    gpx = gpxpy.parse(content.decode("utf-8"))

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

    for track in gpx.tracks:
        for segment in track.segments:

            prev_point = None
            last_alt = None

            for point in segment.points:

                # Start time
                if start_time is None:
                    start_time = point.time

                # Samples
                samples["time"].append(point.time.isoformat() if point.time else None)
                samples["lat"].append(point.latitude)
                samples["lon"].append(point.longitude)
                samples["alt"].append(point.elevation)

                # HR
                hr = None
                if point.extensions:
                    for ext in point.extensions:
                        if "hr" in ext.tag.lower():
                            hr = int(ext.text)
                samples["hr"].append(hr)

                # Distance
                if prev_point:
                    summary["distance_m"] += point.distance_3d(prev_point)
                prev_point = point

                # Elevation gain/loss
                alt = point.elevation
                if last_alt is not None:
                    diff = alt - last_alt
                    if diff > 0:
                        summary["elevation_gain_m"] += diff
                    else:
                        summary["elevation_loss_m"] += abs(diff)
                last_alt = alt

                # Duration
                if start_time and point.time:
                    summary["duration_sec"] = (point.time - start_time).total_seconds()

    return {
        "summary": summary,
        "samples": samples,
        "device": {},
        "start_time": start_time,
        "type": activity_type
    }
