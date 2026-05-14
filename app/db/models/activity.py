from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

# -------------------------
# BLOQUE 1: RESUMEN
# -------------------------
class ActivitySummary(BaseModel):
    duration_sec: int
    distance_m: Optional[float] = None
    elevation_gain_m: Optional[float] = None
    elevation_loss_m: Optional[float] = None
    avg_hr: Optional[int] = None
    max_hr: Optional[int] = None
    avg_power: Optional[int] = None
    max_power: Optional[int] = None
    calories: Optional[int] = None
    avg_pace_sec_per_km: Optional[float] = None

# -------------------------
# BLOQUE 2: MUESTRAS
# -------------------------
class ActivitySamples(BaseModel):
    time: Optional[List[Optional[str]]] = None
    lat: Optional[List[Optional[float]]] = None
    lon: Optional[List[Optional[float]]] = None
    alt: Optional[List[Optional[float]]] = None
    hr: Optional[List[Optional[int]]] = None
    pace: Optional[List[Optional[float]]] = None
    power: Optional[List[Optional[int]]] = None

# -------------------------
# BLOQUE 3: DISPOSITIVO
# -------------------------
class ActivityDevice(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    firmware: Optional[str] = None

# -------------------------
# BLOQUE 4: COMPARACIÓN PLAN VS REAL
# -------------------------
class ActivityComparison(BaseModel):
    status: str
    duration_pct: float
    intensity_shift: Optional[int]
    volume_pct: Optional[float]
    dplus_pct: Optional[float]
    load_score: Optional[int]

# -------------------------
# BLOQUE 5: SESIÓN DEL PLAN
# -------------------------
class LinkedSession(BaseModel):
    session_id: Optional[str]
    date: Optional[str]
    matched: bool = False

# -------------------------
# BLOQUE 6: ACTIVIDAD COMPLETA
# -------------------------
class Activity(BaseModel):
    id: str
    user_id: int
    source: str
    type: str
    file_type: Optional[str] = None
    start_time: datetime

    summary: ActivitySummary
    samples: Optional[ActivitySamples] = None
    device: Optional[ActivityDevice] = None
    comparison: Optional[ActivityComparison] = None
    linked_session: Optional[LinkedSession] = None

    # Campos adicionales
    rpe: Optional[int] = None
    tss: Optional[float] = None
    notes: Optional[str] = None
    perceived_recovery: Optional[int] = None
