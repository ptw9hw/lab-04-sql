-- Select a subset of user and post details using a JOIN and a WHERE filter
SELECT 
    users.username, 
    users.email, 
    posts.title, 
    posts.body, 
    posts.created_at
FROM users
JOIN posts ON users.user_id = posts.user_id
WHERE posts.title LIKE '%Data%';
