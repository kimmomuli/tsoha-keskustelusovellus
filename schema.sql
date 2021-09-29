CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin INTEGER,
    visible INTEGER
);

CREATE TABLE topic (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users ON DELETE CASCADE,
    title TEXT
);

CREATE TABLE thread (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topic ON DELETE CASCADE,
    thread_title TEXT, 
    created_at TIMESTAMP,
    owner_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES thread ON DELETE CASCADE,
    message TEXT,
    owner_id INTEGER REFERENCES users ON DELETE CASCADE
);

