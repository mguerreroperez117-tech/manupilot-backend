from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/home", tags=["Home"])

@router.get("/")
def get_home():
    return {
        "objetivoPrincipal": {
            "nombre": "Trail 25K Sierra Nevada",
            "distancia": 25,
            "desnivelPositivo": 1200,
            "desnivelNegativo": 800,
            "fecha": "2026-09-14"
        },
        "objetivosSecundarios": [
            {
                "nombre": "Trail 12K Marbella",
                "distancia": 12,
                "desnivelPositivo": 450,
                "desnivelNegativo": 430,
                "fecha": "2026-06-10"
            },
            {
                "nombre": "Cross 10K Mijas",
                "distancia": 10,
                "desnivelPositivo": 300,
                "desnivelNegativo": 290,
                "fecha": "2026-05-28"
            }
        ],
        "entrenoHoy": {
            "titulo": "Rodaje suave",
            "detalle": "45 min en Z2",
            "tipo": "correr",
            "ritmo": "5:45–6:10"
        },
        "entrenoManana": {
            "titulo": "Series 6×800m",
            "detalle": "Z4 — Rec: 2 min",
            "tipo": "correr"
        },
        "progreso": {
            "entrenosPrevistos": 5,
            "entrenosCompletados": 4,
            "kmsPrevistos": 42,
            "kmsCompletados": 40,
            "desnivelPrevisto": 1200,
            "desnivelCompletado": 800
        }
    }
