# api_server.py
from flask import Flask, request, jsonify
import random

from db_connection import create_connection, close_connection, mysql  # Import the connection functions

app = Flask(__name__)

@app.route('/random_word', methods=['GET'])
def get_random_word():
    conn = None
    cursor = None
    try:
        # Connect to the database using the function from db_connection.py
        conn = create_connection()
        if conn is None:
            return jsonify({'error': 'Failed to connect to the database'}), 500

        cursor = conn.cursor()
        # Fetch both word and type from the database
        cursor.execute("SELECT word, type FROM words")
        words = cursor.fetchall()
        if words:
            random_word, word_type = random.choice(words)  # Fetch word and type
            return jsonify({'word': random_word, 'type': word_type})  # Return both word and type as JSON
        else:
            return jsonify({'error': 'No words found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        # Close the database connection using the function from db_connection.py
        close_connection(conn, cursor)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/add_word', methods=['POST'])
def add_word():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    new_word = data.get('word')
    word_type = data.get('type')

    if not username or not password or not new_word or not word_type:
        return jsonify({'error': 'Missing parameters'}), 400

    conn = None
    cursor = None
    try:
        # Connect to the database using the function from db_connection.py
        conn = create_connection()
        if conn is None:
            return jsonify({'error': 'Failed to connect to the database'}), 500

        cursor = conn.cursor()

        # Check admin credentials
        cursor.execute("SELECT * FROM admin WHERE username = %s AND pass = %s", (username, password))
        admin = cursor.fetchone()

        if admin:
            # Insert new word into the database
            cursor.execute("INSERT INTO words (word, type) VALUES (%s, %s)", (new_word, word_type))
            conn.commit()
            return jsonify({'message': 'Word added successfully'}), 200
        else:
            return jsonify({'error': 'Invalid admin credentials'}), 403

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
