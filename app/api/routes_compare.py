from fastapi import APIRouter
from app.services.comparison import compare_plan_vs_real

router = APIRouter()

@router.post("/compare")
def compare(planned: dict, actual: dict):
    return compare_plan_vs_real(planned, actual)
