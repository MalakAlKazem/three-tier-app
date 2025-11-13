-- Create the messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO messages (text) VALUES 
    ('Hello from the database! This is a three-tier application.'),
    ('Docker makes containerization easy!'),
    ('Python Flask is great for building APIs.');

-- Create a simple view to get the latest message
CREATE VIEW latest_message AS
SELECT id, text, created_at 
FROM messages 
ORDER BY created_at DESC 
LIMIT 1;