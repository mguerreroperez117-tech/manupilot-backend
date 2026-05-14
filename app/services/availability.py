def get_user_availability(user_id):
    # leer de BD o frontend
    return {
        "days_per_week": 4,
        "daily_time": {
            "monday": "short",
            "tuesday": "medium",
            "wednesday": "rest",
            "thursday": "long",
            "friday": "short",
            "saturday": "long",
            "sunday": "rest"
        },
        "terrain_preferences": {
            "tuesday": "asphalt",
            "thursday": "trail",
            "saturday": "trail"
        },
        "strength_days": ["monday", "thursday"]
    }
