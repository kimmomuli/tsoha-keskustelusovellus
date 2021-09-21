CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin INTEGER,
    visible INTEGER
);

CREATE TABLE topic (
    id SERIAL PRIMARY KEY
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY
);

