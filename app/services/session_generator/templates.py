"""
Plantillas completas para 10K, 21K y Trail.
Organizadas por:
- objetivo
- fase (base, build, peak, taper)
- tipo de sesión

Cada plantilla contiene:
- tipo de sesión (run, strength, technique, mobility)
- intensidad o bloques
- duración base (rango)
- terreno
- desnivel
- fuerza integrada
- técnica integrada
"""

TEMPLATES = {

    # ============================================================
    # =========================== 10K =============================
    # ============================================================

    "10k": {

        "base": {
            "easy": {
                "name": "Rodaje suave",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (40, 60),
                "terrain": "asphalt",
                "strength": None,
                "technique": None
            },
            "easy_progressive": {
                "name": "Rodaje progresivo",
                "type": "run",
                "blocks": [
                    {"duration_min": 20, "intensity": "Z2"},
                    {"duration_min": 10, "intensity": "Z3"}
                ],
                "terrain": "asphalt",
                "strength": None,
                "technique": None
            },
            "long_run": {
                "name": "Tirada larga base",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (60, 90),
                "terrain": "asphalt",
                "strength": None,
                "technique": None
            },
            "strength_general": {
                "name": "Fuerza general",
                "type": "strength",
                "exercises": [
                    {"name": "sentadilla", "sets": 3, "reps": 10},
                    {"name": "zancadas", "sets": 3, "reps": 10},
                    {"name": "peso muerto rumano", "sets": 3, "reps": 8},
                    {"name": "core plancha", "duration_sec": 40}
                ]
            },
            "technique": {
                "name": "Técnica de carrera",
                "type": "technique",
                "drills": [
                    {"name": "skipping", "duration_sec": 20},
                    {"name": "butt kicks", "duration_sec": 20},
                    {"name": "multisaltos", "duration_sec": 20}
                ]
            }
        },

        "build": {
            "tempo": {
                "name": "Tempo controlado",
                "type": "run",
                "blocks": [
                    {"duration_min": 10, "intensity": "Z2"},
                    {"duration_min": 20, "intensity": "Z3"},
                    {"duration_min": 10, "intensity": "Z2"}
                ],
                "terrain": "asphalt",
                "strength": None,
                "technique": None
            },
            "intervals": {
                "name": "Series 10K",
                "type": "run",
                "intervals": [
                    {
                        "work": {"duration_min": 3, "intensity": "Z4"},
                        "rest": {"duration_min": 2, "intensity": "Z2"}
                    }
                ],
                "reps": 5,
                "terrain": "asphalt",
                "strength": None,
                "technique": [
                    {"name": "skipping", "duration_sec": 20}
                ]
            },
            "long_run": {
                "name": "Tirada larga build",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (70, 100),
                "terrain": "asphalt",
                "strength": None,
                "technique": None
            },
            "strength_specific": {
                "name": "Fuerza específica 10K",
                "type": "strength",
                "exercises": [
                    {"name": "sentadilla", "sets": 4, "reps": 6},
                    {"name": "zancadas", "sets": 3, "reps": 8},
                    {"name": "saltos pliométricos", "sets": 3, "reps": 10},
                    {"name": "core plancha lateral", "duration_sec": 30}
                ]
            }
        },

        "peak": {
            "race_pace": {
                "name": "Ritmo competición",
                "type": "run",
                "blocks": [
                    {"duration_min": 5, "intensity": "Z2"},
                    {"duration_min": 15, "intensity": "Z4"},
                    {"duration_min": 5, "intensity": "Z2"}
                ],
                "terrain": "asphalt"
            },
            "intervals_sharpening": {
                "name": "Series afinamiento",
                "type": "run",
                "intervals": [
                    {
                        "work": {"duration_min": 2, "intensity": "Z5"},
                        "rest": {"duration_min": 2, "intensity": "Z2"}
                    }
                ],
                "reps": 4,
                "terrain": "asphalt"
            },
            "short_long_run": {
                "name": "Tirada larga corta",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (50, 70),
                "terrain": "asphalt"
            }
        },

        "taper": {
            "easy": {
                "name": "Rodaje suave taper",
                "type": "run",
                "intensity": "Z1",
                "duration_range": (30, 45),
                "terrain": "asphalt"
            },
            "race_pace_short": {
                "name": "Ritmo competición corto",
                "type": "run",
                "blocks": [
                    {"duration_min": 5, "intensity": "Z2"},
                    {"duration_min": 8, "intensity": "Z4"},
                    {"duration_min": 5, "intensity": "Z1"}
                ],
                "terrain": "asphalt"
            },
            "mobility": {
                "name": "Movilidad y activación",
                "type": "mobility",
                "drills": [
                    {"name": "movilidad cadera", "duration_sec": 30},
                    {"name": "movilidad tobillo", "duration_sec": 30}
                ]
            }
        }
    },

    # ============================================================
    # =========================== 21K =============================
    # ============================================================

    "21k": {
        "base": {
            "easy": {
                "name": "Rodaje suave",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (50, 70),
                "terrain": "asphalt"
            },
            "long_run": {
                "name": "Tirada larga base",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (80, 120),
                "terrain": "asphalt"
            },
            "strength_general": {
                "name": "Fuerza general 21K",
                "type": "strength",
                "exercises": [
                    {"name": "sentadilla", "sets": 3, "reps": 10},
                    {"name": "zancadas", "sets": 3, "reps": 10},
                    {"name": "peso muerto rumano", "sets": 3, "reps": 8},
                    {"name": "core plancha", "duration_sec": 40}
                ]
            }
        },
        "build": {
            "tempo": {
                "name": "Tempo medio",
                "type": "run",
                "blocks": [
                    {"duration_min": 15, "intensity": "Z2"},
                    {"duration_min": 25, "intensity": "Z3"},
                    {"duration_min": 10, "intensity": "Z2"}
                ],
                "terrain": "asphalt"
            },
            "intervals": {
                "name": "Series 21K",
                "type": "run",
                "intervals": [
                    {
                        "work": {"duration_min": 4, "intensity": "Z4"},
                        "rest": {"duration_min": 2, "intensity": "Z2"}
                    }
                ],
                "reps": 4,
                "terrain": "asphalt"
            },
            "long_run": {
                "name": "Tirada larga build",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (100, 140),
                "terrain": "asphalt"
            }
        },
        "peak": {
            "race_pace": {
                "name": "Ritmo competición 21K",
                "type": "run",
                "blocks": [
                    {"duration_min": 10, "intensity": "Z2"},
                    {"duration_min": 25, "intensity": "Z4"},
                    {"duration_min": 10, "intensity": "Z2"}
                ],
                "terrain": "asphalt"
            }
        },
        "taper": {
            "easy": {
                "name": "Rodaje suave taper",
                "type": "run",
                "intensity": "Z1",
                "duration_range": (30, 45),
                "terrain": "asphalt"
            }
        }
    },

    # ============================================================
    # =========================== TRAIL ===========================
    # ============================================================

    "trail": {
        "base": {
            "easy_trail": {
                "name": "Rodaje suave trail",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (60, 120),
                "terrain": "trail",
                "elevation": "medium"
            },
            "hike_run": {
                "name": "Caminata + trote",
                "type": "run",
                "blocks": [
                    {"duration_min": 10, "intensity": "Z1"},
                    {"duration_min": 10, "intensity": "Z2"}
                ],
                "terrain": "trail",
                "elevation": "medium"
            },
            "strength_excentric": {
                "name": "Fuerza excéntrica trail",
                "type": "strength",
                "exercises": [
                    {"name": "sentadilla búlgara", "sets": 3, "reps": 8},
                    {"name": "peso muerto rumano", "sets": 3, "reps": 8},
                    {"name": "gemelos excéntricos", "sets": 3, "reps": 15},
                    {"name": "core plancha lateral", "duration_sec": 30}
                ]
            },
            "technique_downhill": {
                "name": "Técnica de bajadas",
                "type": "technique",
                "drills": [
                    {"name": "bajadas controladas", "duration_min": 5},
                    {"name": "cambios de apoyo", "duration_min": 5}
                ]
            }
        },

        "build": {
            "hill_repeats": {
                "name": "Cuestas",
                "type": "run",
                "subtype": "hill",
                "reps": 6,
                "hill_interval": {"duration_min": 2, "intensity": "Z4"},
                "rest": {"duration_min": 3, "intensity": "Z2"},
                "terrain": "trail",
                "elevation": "high"
            },
            "tempo_uphill": {
                "name": "Tempo en subida",
                "type": "run",
                "blocks": [
                    {"duration_min": 10, "intensity": "Z2"},
                    {"duration_min": 15, "intensity": "Z3"},
                    {"duration_min": 10, "intensity": "Z2"}
                ],
                "terrain": "trail",
                "elevation": "high"
            },
            "long_run_trail": {
                "name": "Tirada larga trail",
                "type": "run",
                "subtype": "long_run",
                "intensity": "Z2",
                "duration_range": (90, 180),
                "terrain": "trail",
                "elevation": "high"
            }
        },

        "peak": {
            "race_specific": {
                "name": "Específico trail",
                "type": "run",
                "blocks": [
                    {"duration_min": 20, "intensity": "Z2"},
                    {"duration_min": 20, "intensity": "Z3"},
                    {"duration_min": 20, "intensity": "Z2"}
                ],
                "terrain": "trail",
                "elevation": "high"
            },
            "long_run_vertical": {
                "name": "Tirada larga vertical",
                "type": "run",
                "intensity": "Z2",
                "duration_range": (120, 180),
                "terrain": "trail",
                "elevation": "high"
            }
        },

        "taper": {
            "easy_trail": {
                "name": "Rodaje suave trail",
                "type": "run",
                "intensity": "Z1",
                "duration_range": (40, 60),
                "terrain": "trail"
            },
            "mobility": {
                "name": "Movilidad trail",
                "type": "mobility",
                "drills": [
                    {"name": "movilidad cadera", "duration_sec": 30},
                    {"name": "movilidad tobillo", "duration_sec": 30}
                ]
            }
        }
    }
}
