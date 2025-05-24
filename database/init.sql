CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    gdp FLOAT,
    social_support FLOAT,
    health FLOAT,
    freedom FLOAT,
    trust FLOAT,
    generosity FLOAT,
    dystopia FLOAT,
    year INT,
    predicted_score FLOAT
);
