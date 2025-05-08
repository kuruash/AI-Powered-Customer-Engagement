import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# PostgreSQL Connection Details (Loaded from .env)
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

# Connect to PostgreSQL
def connect_db():
    """Connect to the database with error handling."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None


# Test database connection
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        conn.close()


# Insert a new user
def insert_user(name, email, phone, company):
    conn = connect_db()
    cur = conn.cursor()
    sql = "INSERT INTO users (name, email, phone, company) VALUES (%s, %s, %s, %s) RETURNING id;"
    cur.execute(sql, (name, email, phone, company))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

# Fetch all users
def get_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

# Test the functions
'''
if __name__ == "__main__":
    user_id = insert_user("John Doe", "john@example.com", "+123456789", "OpenAI Inc.")
    print(f"✅ User inserted with ID: {user_id}")

    users = get_users()
    print("📊 Users in Database:", users)
'''

def get_all_users():
    """Fetch all users from the database"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    conn.close()
    return users

# Test retrieving users
# print("📊 Users in Database:", get_all_users())

def insert_conversation(user_id, message, response):
    """Store chatbot conversations in the database."""
    conn = connect_db()
    cur = conn.cursor()
    sql = "INSERT INTO conversations (user_id, message, response) VALUES (%s, %s, %s);"
    cur.execute(sql, (user_id, message, response))
    conn.commit()
    cur.close()
    conn.close()

def get_conversation_history(user_id):
    """Fetch all messages for a specific user."""
    conn = connect_db()
    cur = conn.cursor()
    sql = "SELECT message, response, timestamp FROM conversations WHERE user_id = %s ORDER BY timestamp DESC;"
    cur.execute(sql, (user_id,))
    history = cur.fetchall()
    cur.close()
    conn.close()
    return history


def get_user_by_email(email):
    """Fetch user ID and details from the database using email."""
    conn = connect_db()
    cur = conn.cursor()
    sql = "SELECT id, name, phone, company FROM users WHERE email = %s;"
    cur.execute(sql, (email,))
    user = cur.fetchone()  # Fetch the first matching user
    
    cur.close()
    conn.close()
    
    return user  # Returns (id, name, phone, company) if found, else None


def get_conversation_history(user_id):
    """Fetch conversation history for a user."""
    conn = connect_db()
    cur = conn.cursor()
    sql = "SELECT message, response, timestamp FROM conversations WHERE user_id = %s ORDER BY timestamp DESC;"
    cur.execute(sql, (user_id,))
    history = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return history
