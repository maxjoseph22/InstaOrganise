DROP TABLE IF EXISTS cross_breeds;

CREATE TABLE cross_breeds (
    id SERIAL PRIMARY KEY,
    breed_name VARCHAR(255),
    count int
);
