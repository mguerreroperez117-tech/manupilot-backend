from sqlalchemy.orm import Session
from sqlalchemy import select

# Modelo SQLAlchemy correcto
from app.db.models.activity_db import ActivityDB

# Sesión de base de datos correcta
from app.database import SessionLocal


# ---------------------------------------------------------
# Guardar actividad en PostgreSQL (SÍNCRONO)
# ---------------------------------------------------------
def save_activity(activity):
    db: Session = SessionLocal()

    db_obj = ActivityDB(
        id=activity.id,
        user_id=activity.user_id,
        source=activity.source,
        type=activity.type,
        file_type=activity.file_type,
        start_time=activity.start_time,

        summary=activity.summary.dict(),
        samples=activity.samples.dict() if activity.samples else None,
        device=activity.device.dict() if activity.device else None,
        comparison=activity.comparison.dict() if activity.comparison else None,
        linked_session=activity.linked_session.dict() if activity.linked_session else None,

        rpe=activity.rpe,
        tss=activity.tss,
        notes=activity.notes,
        perceived_recovery=activity.perceived_recovery
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    db.close()

    return db_obj.id


# ---------------------------------------------------------
# Obtener actividad por ID (SÍNCRONO)
# ---------------------------------------------------------
def get_activity_by_id(activity_id: str):
    db: Session = SessionLocal()

    result = db.execute(
        select(ActivityDB).where(ActivityDB.id == activity_id)
    )

    activity = result.scalar_one_or_none()
    db.close()

    return activity
