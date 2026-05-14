from fastapi import FastAPI

# Routers existentes
from app.api.routes_activities import router as activities_router
from app.api.routes_load import router as load_router
from app.api.routes_plan import router as plan_router
from app.api.routes_sync import router as sync_router
from app.api.routes_compare import router as compare_router
from app.api.routes_admin import router as admin_router
from app.api.routes_home import router as home_router

# Nuevo router de autenticación
from app.api.routes_auth import router as auth_router

# Importar Base y engine para crear tablas
from app.database import Base, engine


# ---------------------------------------------------------
# APP FASTAPI
# ---------------------------------------------------------
app = FastAPI(title="Training Backend")

# ---------------------------------------------------------
# CREAR TABLAS AUTOMÁTICAMENTE
# ---------------------------------------------------------
from app.db.models import user_db

Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------
# RUTAS PRINCIPALES DEL SISTEMA
# ---------------------------------------------------------
app.include_router(activities_router)                 # /activities
app.include_router(load_router)                       # /load
app.include_router(plan_router)                       # /plan
app.include_router(sync_router, prefix="/sync")       # /sync
app.include_router(compare_router, prefix="/plan")    # /plan/...
app.include_router(admin_router)                      # /admin
app.include_router(home_router)                       # /home

# NUEVO: rutas de autenticación

# NUEVO: rutas de autenticación
app.include_router(auth_router, prefix="/auth")


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
