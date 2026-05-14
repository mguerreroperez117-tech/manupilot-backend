import uuid
from app.db.models.activity import Activity


# ---------------------------------------------------------
# FIT → Activity
# ---------------------------------------------------------
def build_activity_from_fit(parsed: dict, user_id: int, source: str) -> Activity:
    return Activity(
        id=str(uuid.uuid4()),
        user_id=user_id,
        source=source,
        type=parsed.get("type", "unknown"),
        file_type="fit",
        start_time=parsed.get("start_time"),
        summary=parsed.get("summary", {}),
        samples=parsed.get("samples", {}),
        device=parsed.get("device", {}),
        comparison=None,
        linked_session=None,
        rpe=None,
        tss=None,
        notes=None,
        perceived_recovery=None
    )


# ---------------------------------------------------------
# GPX → Activity
# ---------------------------------------------------------
def build_activity_from_gpx(parsed: dict, user_id: int, source: str) -> Activity:
    return Activity(
        id=str(uuid.uuid4()),
        user_id=user_id,
        source=source,
        type=parsed.get("type", "unknown"),
        file_type="gpx",
        start_time=parsed.get("start_time"),
        summary=parsed.get("summary", {}),
        samples=parsed.get("samples", {}),
        device=parsed.get("device", {}),
        comparison=None,
        linked_session=None,
        rpe=None,
        tss=None,
        notes=None,
        perceived_recovery=None
    )


# ---------------------------------------------------------
# TCX → Activity
# ---------------------------------------------------------
def build_activity_from_tcx(parsed: dict, user_id: int, source: str) -> Activity:
    return Activity(
        id=str(uuid.uuid4()),
        user_id=user_id,
        source=source,
        type=parsed.get("type", "unknown"),
        file_type="tcx",
        start_time=parsed.get("start_time"),
        summary=parsed.get("summary", {}),
        samples=parsed.get("samples", {}),
        device=parsed.get("device", {}),
        comparison=None,
        linked_session=None,
        rpe=None,
        tss=None,
        notes=None,
        perceived_recovery=None
    )
