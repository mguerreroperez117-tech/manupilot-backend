from fastapi import APIRouter, UploadFile, File, HTTPException

# Rutas correctas según tu estructura actual
from app.services.fit_parser import parse_fit_file
from app.services.gpx_parser import parse_gpx_file
from app.services.tcx_parser import parse_tcx_file

router = APIRouter()

@router.post("/upload")
async def upload_activity(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = await file.read()

    if filename.endswith(".fit"):
        data = parse_fit_file(content)

    elif filename.endswith(".gpx"):
        data = parse_gpx_file(content)

    elif filename.endswith(".tcx"):
        data = parse_tcx_file(content)

    else:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Usa FIT, GPX o TCX."
        )

    return {
        "status": "ok",
        "parsed": data
    }

