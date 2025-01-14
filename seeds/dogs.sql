DROP TABLE IF EXISTS dogs;

CREATE TABLE dogs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    breed VARCHAR(255),
    purebreed boolean,
    mix boolean,
    age int,
    sex VARCHAR(255),
    location VARCHAR(255),
    personality text,
    likes int,
    comments int,
    link_to_post VARCHAR(255),
    photo VARCHAR(255) DEFAULT NULL


);

