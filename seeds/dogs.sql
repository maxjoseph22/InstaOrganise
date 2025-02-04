DROP TABLE IF EXISTS dogs;

CREATE TABLE dogs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    breed VARCHAR(255),
    purebreed BOOLEAN,
    mix BOOLEAN,
    age INT,
    sex VARCHAR(255),
    location VARCHAR(255),
    personality TEXT,
    likes INT,
    comments INT,
    link_to_post VARCHAR(255),
    photo VARCHAR(255) DEFAULT NULL,
    video BOOLEAN,
    breed_id INT,
    CONSTRAINT fk_breed FOREIGN KEY (breed_id)
        REFERENCES breeds (id)
        ON DELETE CASCADE,
    cross_breed_id INT,
    CONSTRAINT fk_cross_breed FOREIGN KEY (cross_breed_id)
        REFERENCES cross_breeds (id)
        ON DELETE CASCADE
);

