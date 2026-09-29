-- Step 1: Create Your Database Schema

-- Drop tables if they already exist to allow clean re-runs
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- Create the 'users' table with 4 columns
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL
);

-- Create the 'posts' table with 4 columns and a foreign key referencing 'users'
CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Step 2: Add at least 10 INSERT statements for each table

-- Insert 10 rows into 'users'
INSERT INTO users (user_id, username, email, created_at) VALUES 
(1, 'alex_d', 'alex@example.com', '2026-09-01 08:30:00'),
(2, 'sarah_c', 'sarah@example.com', '2026-09-02 09:15:00'),
(3, 'mike_b', 'mike@example.com', '2026-09-03 10:00:00'),
(4, 'emily_w', 'emily@example.com', '2026-09-04 11:20:00'),
(5, 'chris_m', 'chris@example.com', '2026-09-05 12:45:00'),
(6, 'jess_k', 'jess@example.com', '2026-09-06 14:10:00'),
(7, 'david_l', 'david@example.com', '2026-09-07 15:30:00'),
(8, 'amanda_p', 'amanda@example.com', '2026-09-08 16:05:00'),
(9, 'ryan_t', 'ryan@example.com', '2026-09-09 17:50:00'),
(10, 'olivia_h', 'olivia@example.com', '2026-09-10 18:25:00');

-- Insert 10 rows into 'posts' (all user_ids reference valid primary keys in 'users')
INSERT INTO posts (post_id, user_id, title, body) VALUES 
(101, 1, 'First Post', 'Hello world! This is my very first post on the platform.'),
(102, 1, 'SQL Tips', 'Learning relational databases is super rewarding once it clicks.'),
(103, 2, 'Morning Thoughts', 'Woke up early today to get a head start on data science assignments.'),
(104, 3, 'Python vs SQL', 'Both are essential tools for any modern data pipeline.'),
(105, 4, 'Weekend Hiking', 'Planning a trip to the Blue Ridge mountains this weekend.'),
(106, 5, 'Data Cleaning', 'Spent half the day dealing with missing values in pandas. Good times!'),
(107, 6, 'Coffee & Code', 'There is nothing better than a fresh cup of coffee and some clean code.'),
(108, 7, 'Database Normalization', 'First, second, and third normal form explained simply.'),
(109, 8, 'Git Workflow', 'Always commit early and often to avoid merge conflicts.'),
(110, 10, 'Project Kickoff', 'Excited to start working on the new team database project!');
