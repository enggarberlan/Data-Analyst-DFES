CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY,
    location_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS incidents (
    incident_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    location_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    response_time_minutes REAL,
    units_dispatched INTEGER NOT NULL,
    response_time_review INTEGER NOT NULL,

    FOREIGN KEY (location_id)
        REFERENCES locations(location_id)
);