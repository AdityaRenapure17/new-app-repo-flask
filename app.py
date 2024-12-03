from flask import Flask, request, jsonify
import pymysql
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database connection settings
DB_HOST = "10.38.92.90"  # Replace with your MySQL server IP
DB_USER = "admin"
DB_PASSWORD = "Nutanix/4u"
DB_NAME = "demo_app"

def get_db_connection():
    """Create and return a database connection."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def home():
    """Root endpoint to verify the app is running."""
    return "Welcome to the Demo App! Available endpoints: /create, /read, /update, /delete"

@app.route('/create', methods=['POST'])
def create():
    """Endpoint to create a new record."""
    try:
        # Debug log for incoming request data
        app.logger.debug("Request data: %s", request.json)

        # Extract and validate the request data
        data = request.json
        if not data or 'name' not in data:
            app.logger.error("Invalid input: %s", data)
            return jsonify({"error": "Invalid input"}), 400

        # Insert the data into the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO demo_table (name) VALUES (%s)", (data['name'],))
            connection.commit()
        connection.close()

        return jsonify({"message": "Record created"}), 201

    except Exception as e:
        app.logger.error("Error in /create: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read():
    """Endpoint to read all records."""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM demo_table")
            rows = cursor.fetchall()
        connection.close()

        return jsonify(rows), 200

    except Exception as e:
        app.logger.error("Error in /read: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route('/update', methods=['PUT'])
def update():
    """Endpoint to update an existing record."""
    try:
        data = request.json
        if not data or 'id' not in data or 'name' not in data:
            app.logger.error("Invalid input: %s", data)
            return jsonify({"error": "Invalid input"}), 400

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("UPDATE demo_table SET name=%s WHERE id=%s", (data['name'], data['id']))
            connection.commit()
        connection.close()

        return jsonify({"message": "Record updated"}), 200

    except Exception as e:
        app.logger.error("Error in /update: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route('/delete', methods=['DELETE'])
def delete():
    """Endpoint to delete a record."""
    try:
        data = request.json
        if not data or 'id' not in data:
            app.logger.error("Invalid input: %s", data)
            return jsonify({"error": "Invalid input"}), 400

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM demo_table WHERE id=%s", (data['id'],))
            connection.commit()
        connection.close()

        return jsonify({"message": "Record deleted"}), 200

    except Exception as e:
        app.logger.error("Error in /delete: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
