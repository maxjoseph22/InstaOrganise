DROP TABLE IF EXISTS mixed_breeds;

CREATE TABLE mixed_breeds (
    id SERIAL PRIMARY KEY,
    breed_name VARCHAR(255),
    count int
);
