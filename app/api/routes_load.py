from fastapi import APIRouter
from app.services.analysis import calculate_training_load, calculate_zones_distribution

router = APIRouter(prefix="/load", tags=["load"])

@router.get("/")
def get_load():
    return {
        "training_load": calculate_training_load(),
        "zones": calculate_zones_distribution()
    }
