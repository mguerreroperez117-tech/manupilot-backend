CREATE TABLE IF NOT EXISTS activities (
    id TEXT PRIMARY KEY,
    source TEXT,
    type TEXT,
    start_time TEXT,
    duration_sec INTEGER,
    distance_m REAL,
    elevation_gain_m REAL,
    avg_hr INTEGER,
    max_hr INTEGER,
    rpe INTEGER,
    tss REAL,
    calories INTEGER,
    notes TEXT,
    perceived_recovery INTEGER
);

-- Tabla de configuración del módulo adaptativo
CREATE TABLE IF NOT EXISTS adaptive_config (
    key TEXT PRIMARY KEY,
    value REAL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
