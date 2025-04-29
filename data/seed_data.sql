-- Clear existing users (if any)
DELETE FROM users;

-------------------------------------------------
-- Insert 1 users to keep record when users are not logged in
-------------------------------------------------
INSERT INTO users(id, username, password_hash) VALUES
    (1, 'guest', 'scrypt:32768:8:1$MPut1LWmAa0itDuu$8e59b189c39a66479f815ba59e42e82fa51725f02dfc8e2083d36172dd63ead9623ed7eeac8edb80d5213200e53238ccfe0dee66bff406035b37348c8caca59e');

-- Clean up existing test data
DELETE FROM user_statistics;

INSERT INTO user_statistics(user_id, high_score, level) values(1, 1, 1);
