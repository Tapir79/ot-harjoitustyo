CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE user_statistics(
    id INTEGER PRIMARY KEY,
    high_score INTEGER,
    level INTEGER,
    created_at TEXT DEFAULT (DATETIME('now')),
    updated_at TEXT DEFAULT (DATETIME('now')), 
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

-- 3 top high scores
CREATE VIEW general_statistics AS
    SELECT u.username, us.high_score, us.level
    FROM users u
    JOIN user_statistics us ON u.id = us.user_id
    ORDER BY us.high_score DESC, us.level ASC
    LIMIT 3;