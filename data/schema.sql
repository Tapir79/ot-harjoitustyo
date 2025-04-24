CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE user_statistics(
    id INTEGER PRIMARY KEY,
    high_score INTEGER,
    level INTEGER,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

-- 5 top high scores
CREATE VIEW general_statistics AS
    SELECT u.username, us.high_score, us.level
    FROM users u
    JOIN user_statistics us ON u.id = us.user_id
    ORDER BY us.high_score DESC
    LIMIT 5;