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

INSERT INTO dogs (name, breed, purebreed, mix, age, sex, location, personality, likes, comments, link_to_post, photo) VALUES ('Benny', 'Poodle', true, false, 5, 'Boy', 'London, UK', 'Likes to chew sticks', 1000, 200, 'www.instagram.com/ksdf9sfj', NULL);