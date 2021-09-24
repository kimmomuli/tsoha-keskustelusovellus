CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin INTEGER,
    visible INTEGER
);

CREATE TABLE topic (
    id SERIAL PRIMARY KEY,
    title TEXT
);

CREATE TABLE thread (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topic,
    thread_title TEXT, 
    created_at TIMESTAMP,
    owner_id INTEGER REFERENCES users 
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES thread ON DELETE CASCADE,
    message TEXT
);

