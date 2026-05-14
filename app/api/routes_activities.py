from fastapi import APIRouter, UploadFile, File, Form
from typing import Literal

# MODELO Pydantic (correcto)
from app.db.models.activity import Activity

# REPOSITORIO
from app.db.repositories.activity_repository import save_activity, get_activity_by_id

# Parsers
from app.services.fit_parser import parse_fit_file
from app.services.gpx_parser import parse_gpx_file
from app.services.tcx_parser import parse_tcx_file

# Builders
from app.services.activity_builder import (
    build_activity_from_fit,
    build_activity_from_gpx,
    build_activity_from_tcx
)

router = APIRouter(prefix="/activities", tags=["activities"])


# ---------------------------------------------------------
# 1) Guardar actividad ya procesada
# ---------------------------------------------------------
@router.post("/save")
async def save_activity_endpoint(activity: Activity):
    activity_id = await save_activity(activity)
    return {"status": "ok", "activity_id": activity_id}


# ---------------------------------------------------------
# 2) Subir archivo .fit / .gpx / .tcx
# ---------------------------------------------------------
@router.post("/upload-file")
async def upload_activity_file(
    user_id: int = Form(...),
    source: Literal["garmin", "coros", "suunto", "polar", "apple"] = Form(...),
    file: UploadFile = File(...)
):
    content = await file.read()
    filename = file.filename.lower()

    # Detectar tipo
    if filename.endswith(".fit"):
        file_type = "fit"
        parsed = parse_fit_file(content)
        activity = build_activity_from_fit(parsed, user_id, source)

    elif filename.endswith(".gpx"):
        file_type = "gpx"
        parsed = parse_gpx_file(content)
        activity = build_activity_from_gpx(parsed, user_id, source)

    elif filename.endswith(".tcx"):
        file_type = "tcx"
        parsed = parse_tcx_file(content)
        activity = build_activity_from_tcx(parsed, user_id, source)

    else:
        return {"error": "Formato no soportado. Usa .fit, .gpx o .tcx"}

    # Guardar en PostgreSQL
    activity_id = await save_activity(activity)

    return {
        "status": "saved",
        "file_type": file_type,
        "activity_id": activity_id
    }


# ---------------------------------------------------------
# 3) Obtener actividad por ID
# ---------------------------------------------------------
@router.get("/{activity_id}")
async def get_activity(activity_id: str):
    activity = await get_activity_by_id(activity_id)
    if not activity:
        return {"error": "Activity not found"}
    return activity
