from datetime import date
from typing import Optional, List, Literal
from pydantic import BaseModel


class PlanGoal(BaseModel):
    type: Literal["10k", "21k", "trail", "health", "strength"]
    target_date: date
    target_time: Optional[str] = None
    target_distance_km: Optional[float] = None
    target_elevation_pos_m: Optional[int] = None
    target_elevation_neg_m: Optional[int] = None


class Milestone(BaseModel):
    name: str
    date: date
    type: Literal["performance_test", "deload_week", "checkpoint"]
    notes: Optional[str] = None


class InitialAssessment(BaseModel):
    required: bool = True
    completed: bool = False
    protocol: Literal["3k_time_trial", "20min_test", "strength_basic"]


class PeriodicTest(BaseModel):
    interval_weeks: int
    type: Literal["threshold_test", "strength_test", "trail_specific"]
    description: Optional[str] = None


class StrengthExercise(BaseModel):
    name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_sec: Optional[int] = None
    description: Optional[str] = None
    video_url: Optional[str] = None


class NutritionAdvice(BaseModel):
    pre: Optional[str] = None
    during: Optional[str] = None
    post: Optional[str] = None


class PlanSession(BaseModel):
    date: date
    name: str
    type: Literal["run", "strength", "technique", "mobility", "rest"]
    subtype: Optional[str] = None

    duration_min: Optional[int] = None
    intensity: Optional[str] = None
    terrain: Optional[str] = None
    elevation: Optional[str] = None

    blocks: Optional[list] = None
    intervals: Optional[list] = None
    reps: Optional[int] = None

    exercises: Optional[List[StrengthExercise]] = None
    drills: Optional[list] = None

    cancelled: bool = False
    rest: bool = False

    nutrition: Optional[NutritionAdvice] = None

    is_test: bool = False
    is_strength: bool = False


class TrainingPlan(BaseModel):
    user_id: int
    goal: PlanGoal
    milestones: List[Milestone] = []
    initial_assessment: Optional[InitialAssessment] = None
    periodic_tests: List[PeriodicTest] = []

    strength_focus: Optional[str] = None

    sessions: List[PlanSession]
