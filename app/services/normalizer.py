import uuid
from datetime import datetime
from backend.app.models.activity_db import Activity

def normalize_activity(
    source: str,
    type: str,
    start_time: datetime,
    duration_sec: int,
    distance_m: float,
    elevation_gain_m: float,
    avg_hr: int | None,
    max_hr: int | None,
    rpe: int | None = None,
    tss: float | None = None,
    calories: int | None = None,
    notes: str | None = None
) -> Activity:

    return Activity(
        id=str(uuid.uuid4()),
        source=source,
        type=type,
        start_time=start_time,
        duration_sec=duration_sec,
        distance_m=distance_m,
        elevation_gain_m=elevation_gain_m,
        avg_hr=avg_hr,
        max_hr=max_hr,
        rpe=rpe,
        tss=tss,
        calories=calories,
        notes=notes
    )
