from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Crear engine síncrono
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

# Crear sesión síncrona
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos
Base = declarative_base()

# ⭐ IMPORTANTE: importar los modelos ANTES de create_all
from app.db.models import user_db   # ← ESTA LÍNEA ES LA CLAVE

# ⭐ Crear tablas
Base.metadata.create_all(bind=engine)

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
