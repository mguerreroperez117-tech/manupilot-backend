from fastapi import APIRouter
from app.config.config_manager import get_config, update_config

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/config")
def read_config():
    """
    Devuelve la configuración actual del sistema.
    """
    return get_config()


@router.post("/config/update")
def update_system_config(payload: dict):
    """
    Actualiza parámetros de configuración en caliente.
    """
    new_config = update_config(payload)
    return {
        "status": "ok",
        "updated": payload,
        "current_config": new_config
    }
