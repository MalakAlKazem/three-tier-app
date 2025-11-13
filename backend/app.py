from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Database configuration from environment variables
DB_HOST = os.environ.get('DB_HOST', 'database')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'appdb')
DB_USER = os.environ.get('DB_USER', 'dbuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password123')

def get_db_connection():
    """Create and return a database connection"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            logger.info("Successfully connected to database")
            return conn
        except psycopg2.OperationalError as e:
            retry_count += 1
            logger.warning(f"Failed to connect to database (attempt {retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                time.sleep(5)  # Wait 5 seconds before retrying
            else:
                raise

@app.route('/')
def home():
    """Home endpoint to check if API is running"""
    return jsonify({
        "status": "healthy",
        "message": "Backend API is running!",
        "endpoints": {
            "/": "This help message",
            "/api/message": "Get the latest message from database",
            "/api/messages": "Get all messages from database",
            "/api/health": "Health check endpoint"
        }
    })

@app.route('/api/message')
def get_message():
    """Get the latest message from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query to get the latest message
        cursor.execute("SELECT id, text, created_at FROM messages ORDER BY created_at DESC LIMIT 1")
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            return jsonify({
                "success": True,
                "data": {
                    "id": row[0],
                    "text": row[1],
                    "created_at": row[2].isoformat() if row[2] else None
                }
            })
        else:
            return jsonify({
                "success": False,
                "message": "No messages found in database"
            }), 404
            
    except Exception as e:
        logger.error(f"Error fetching message: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/messages')
def get_all_messages():
    """Get all messages from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, text, created_at FROM messages ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        messages = []
        for row in rows:
            messages.append({
                "id": row[0],
                "text": row[1],
                "created_at": row[2].isoformat() if row[2] else None
            })
        
        return jsonify({
            "success": True,
            "data": messages,
            "count": len(messages)
        })
        
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        # Try to connect to database
        conn = get_db_connection()
        conn.close()
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    return jsonify({
        "api": "healthy",
        "database": db_status
    })

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)