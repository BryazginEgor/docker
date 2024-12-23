CREATE TABLE IF NOT EXISTS processed_data (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    data TEXT
);
