from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_passsword = os.environ.get("DBPASS")

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = db_passsword,
        database = "internship_db"
    )
    return connection

@app.route('/api/hello', methods=['GET'])
def hello_world_api():
    return jsonify({
        "status": "success",
        "message": "Hello from Flask"
    })

@app.route('/api/db-check', methods=['GET'])
def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": f"Successfully connected to the database: {db_name[0]}"
        })
    
    except Exception as error:
        return jsonify({
            "status": "error",
            "message": f"Database connection failed! Error: {str(error)}"
        }), 500

@app.route('/api/add-application', methods=['POST'])
def add_application():
    try:
        data = request.get_json()
        comp = data.get('company_name')
        job = data.get('job_title')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO applications (company_name, job_title) VALUES (%s, %s)"

        cursor.execute(query, (comp, job))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": f"Successfully added application for {comp}!"
        }), 201

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": f"Failed to save data. Error: {str(error)}"
        }), 500

@app.route('/api/applications', methods=['GET'])
def get_all_applications():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, company_name, job_title, apply_status FROM applications;")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        applications_list = []
        for row in rows:
            applications_list.append({
                "id": row[0],
                "company_name": row[1],
                "job_title": row[2],
                "apply_status": row[3]
            })

        return jsonify({
            "status": "success",
            "message": applications_list
        }), 200
    
    except Exception as error:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve data. Error: {str(error)}"
        }), 500

@app.route('/api/update-status', methods=['PUT'])
def update_application_status():
    try:
        data = request.get_json()
        app_id = data.get('id')
        new_status = data.get('status')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE applications SET apply_status = %s WHERE id = %s;"
        cursor.execute(query, (new_status, app_id))

        conn.commit()

        rows_affected = cursor.rowcount

        cursor.close()
        conn.close()

        if rows_affected == 0:
            return jsonify({
                "status": "error",
                "message": f"No application found with ID {app_id}." 
            }), 404
        
        return jsonify({
            "status": "success",
            "message": f"Successfully updated application ID {app_id} to '{new_status}'!"
        }), 200
    
    except Exception as error:
        return jsonify({
            "status": "error",
            "message": f"Failed to update status. Error: {str(error)}"
        }), 500

@app.route('/api/delete-application', methods=['DELETE'])
def delete_spplication():
    try:
        data = request.get_json()
        app_id = data.get('id')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM applications WHERE id = %s;"
        cursor.execute(query, (app_id,))

        conn.commit()
        rows_affected = cursor.rowcount

        cursor.close()
        conn.close()

        if rows_affected == 0:
            return jsonify({
                "status": "error",
                "message": f"No application found with ID {app_id}."
            }), 404
        
        return jsonify({
            "status": "success",
            "message": f"Successfully deleted application ID {app_id}!"
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": f"Failed to delete entry. Error: {str(error)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)