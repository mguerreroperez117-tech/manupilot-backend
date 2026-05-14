TRAINING_CONFIG = {

    # ============================================================
    # NUTRICIÓN
    # ============================================================
    "nutrition": {

        # Entrenamiento en ayunas (básico)
        "fasted_training": {
            "enabled": True,
            "max_duration_min": 60,
            "allowed_intensities": ["Z1", "Z2"],
            "exclude_keywords": ["tempo", "interval", "long"]
        },

        # Ayuno avanzado por fase
        "advanced_fasted": {
            "enabled": True,
            "phases": ["base", "build"],
            "max_duration_min": 75,
            "allowed_intensities": ["Z1", "Z2"],
            "progression": {
                "base": "Ayuno suave: sesiones Z1–Z2 cortas.",
                "build": "Ayuno moderado: sesiones Z2 medias.",
                "peak": "Evitar ayuno en fase pico.",
                "taper": "Evitar ayuno en descarga."
            }
        },

        # Carga progresiva de hidratos por fase
        "carb_loading": {
            "base": "Carga ligera de hidratos 2–3 h antes.",
            "build": "Carga moderada de hidratos 3 h antes.",
            "peak": "Carga alta de hidratos 3 h antes.",
            "taper": "Carga reducida de hidratos."
        },

        # Adaptación al calor (básico)
        "heat_adaptation": {
            "enabled": True,
            "months": [6, 7, 8, 9],
            "max_duration_min": 40,
            "pre": "Sesión corta de adaptación al calor: hidrátate bien antes.",
            "during": "Bebe agua cada 10–15 min.",
            "post": "Rehidrata con electrolitos."
        },

        # Adaptación al calor avanzada
        "advanced_heat": {
            "enabled": True,
            "sauna_after_easy": True,
            "overdressing_sessions": ["easy", "tempo"],
            "max_heat_sessions_per_week": 2,
            "notes": {
                "sauna": "10–15 min de sauna tras la sesión para aumentar adaptación.",
                "overdress": "Entrena con ropa extra para elevar la temperatura corporal."
            }
        },

        # Nutrición durante la sesión
        "during_session": {
            "min_duration_for_carbs": 75,
            "carbs_per_hour": "30–60 g de carbohidratos por hora."
        },

        # Nutrición post sesión
        "post_session": {
            "strength": "Proteína 20–30 g + carbohidratos para recuperar.",
            "default": "Proteína + carbohidratos en los 30 min posteriores."
        }
    },

    # ============================================================
    # ENTRENAMIENTO (ZONAS, RITMOS, DESNIVEL, ADAPTATIVO)
    # ============================================================
    "training": {

        # Zonas de entrenamiento
        "zones": {
            "Z1": {"percent": [50, 60]},
            "Z2": {"percent": [60, 70]},
            "Z3": {"percent": [70, 80]},
            "Z4": {"percent": [80, 90]},
            "Z5": {"percent": [90, 100]}
        },

        # Ritmos base por zona
        "paces": {
            "Z1": "6:30/km",
            "Z2": "5:30/km",
            "Z3": "4:50/km",
            "Z4": "4:20/km",
            "Z5": "3:50/km"
        },

        # Ajustes por fatiga (PRS)
        "fatigue_adjustments": {
            "high": 0.85,   # PRS < 5
            "medium": 0.95, # PRS 5–7
            "low": 1.0      # PRS > 7
        },

        # Desnivel por fase (para trail)
        "elevation": {
            "base": 200,
            "build": 400,
            "peak": 600,
            "taper": 150
        },

        # Técnica progresiva por fase
        "technique_progression": {
            "base": ["drills_basic"],
            "build": ["drills_advanced"],
            "peak": ["economy_drills"],
            "taper": ["light_drills"]
        },

        # Ejercicios concretos de técnica
        "technique_drills": {
            "drills_basic": [
                "Skipping suave 3×20 m",
                "Talones al glúteo 3×20 m",
                "Rodillas arriba 3×20 m",
                "Técnica de braceo 2×30 s"
            ],
            "drills_advanced": [
                "Skipping rápido 3×25 m",
                "Multisaltos avanzados 3×15 m",
                "Zancada técnica 3×20 m",
                "Técnica de cadencia 2×1 min"
            ],
            "economy_drills": [
                "Ejercicios de economía de carrera 3×20 m",
                "Respiración diafragmática 2×1 min",
                "Relajación de hombros y brazos 2×30 s"
            ],
            "light_drills": [
                "Skipping suave 2×15 m",
                "Movilidad de tobillo 2×30 s",
                "Activación ligera 2×20 m"
            ]
        },

        # Fuerza periodizada por fase
        "strength_periodization": {
            "base": "general_strength",
            "build": "eccentric_strength",
            "peak": "power_strength",
            "taper": "light_strength"
        },

        # Ejercicios concretos de fuerza por categoría
        "strength_exercises": {

            # Fuerza general (Base)
            "general_strength": [
                {"name": "Sentadilla", "sets": 3, "reps": 10, "percent_1RM": 60, "type": "fuerza general"},
                {"name": "Peso muerto rumano", "sets": 3, "reps": 8, "percent_1RM": 55, "type": "fuerza general"},
                {"name": "Zancadas", "sets": 3, "reps": 12, "percent_1RM": 0, "type": "fuerza general"},
                {"name": "Plancha", "sets": 3, "duration": "45s", "type": "core"}
            ],

            # Fuerza excéntrica (Build)
            "eccentric_strength": [
                {"name": "Sentadilla excéntrica (4s bajada)", "sets": 4, "reps": 6, "percent_1RM": 65, "type": "excéntrica"},
                {"name": "Peso muerto excéntrico", "sets": 4, "reps": 5, "percent_1RM": 60, "type": "excéntrica"},
                {"name": "Saltos excéntricos controlados", "sets": 3, "reps": 8, "type": "pliometría suave"}
            ],

            # Fuerza potencia (Peak)
            "power_strength": [
                {"name": "Saltos pliométricos", "sets": 4, "reps": 6, "type": "potencia"},
                {"name": "Sentadilla con salto", "sets": 3, "reps": 8, "type": "potencia"},
                {"name": "Skipping explosivo", "sets": 3, "duration": "20s", "type": "potencia"}
            ],

            # Fuerza ligera (Taper)
            "light_strength": [
                {"name": "Movilidad dinámica", "sets": 2, "duration": "45s", "type": "ligera"},
                {"name": "Core ligero", "sets": 2, "duration": "30s", "type": "ligera"},
                {"name": "Activación glúteo", "sets": 2, "reps": 12, "type": "ligera"}
            ]
        }
    },

    # ============================================================
    # COMENTARIOS INTELIGENTES
    # ============================================================
    "comments": {

        "types": {
            "easy": "Rodaje suave para favorecer la recuperación y mejorar la base aeróbica.",
            "tempo": "Trabajo de tempo para mejorar el umbral y la economía de carrera.",
            "intervals": "Sesión de intervalos para desarrollar velocidad y VO2max.",
            "long_run": "Tirada larga para mejorar resistencia y eficiencia energética.",
            "trail": "Sesión de trail para trabajar fuerza, técnica y adaptación al terreno.",
            "strength": "Sesión de fuerza para mejorar estabilidad y prevenir lesiones.",
            "technique": "Trabajo técnico para mejorar la eficiencia y la postura."
        },

        "phases": {
            "base": "Seguimos construyendo una base sólida.",
            "build": "Semana de carga progresiva, es normal sentir más fatiga.",
            "peak": "Estamos en fase pico, prioriza calidad y descanso.",
            "taper": "Semana de descarga, reduce estrés y mantén sensaciones."
        },

        "special": {
            "heat": "Sesión de adaptación al calor: hidrátate bien antes, durante y después.",
            "fasted": "Sesión en ayunas: mantén la intensidad baja y desayuna después.",
            "trail_elevation": "Trabaja la técnica en subidas y controla el ritmo en bajadas.",
            "prs_high": "Muy buenas sensaciones, sigue así.",
            "prs_low": "Fatiga elevada, prioriza descanso y buena nutrición."
        }
    }
}

