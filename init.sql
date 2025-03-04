CREATE TABLE mytable (
    id SERIAL PRIMARY KEY,
    data JSONB,
    extra JSONB NOT NULL
);

CREATE TABLE anothertable (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL
);