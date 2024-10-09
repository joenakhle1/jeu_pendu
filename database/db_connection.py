# db_connection.py
import mysql.connector
from mysql.connector import Error

# Database configuration
db_config = {
    'user': 'root',        # Replace with your MySQL username
    'password': '',    # Replace with your MySQL password
    'host': 'localhost',            # Replace with your MySQL host if different
    'database': 'hangman',    # Replace with your MySQL database name
}

# Function to connect to the database
def create_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Error as err:
        print(f"Error: {err}")
        return None

# Function to close the database connection
def close_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        print("MySQL connection closed")
