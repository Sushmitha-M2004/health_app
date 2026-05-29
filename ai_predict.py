from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from ai_predict import predict_health
import pymysql
import os
import re
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database Connection
db = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)

# Home Page

@app.route('/')
def index():

    try:

        cursor = db.cursor()

        cursor.execute("SELECT * FROM patients")

        patients = cursor.fetchall()

        cursor.close()

        return render_template(
            'index.html',
            patients=patients
        )

    except Exception as e:

        return "Database Error: " + str(e)

# =========================
# Add Patient
# =========================

@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        full_name = request.form['full_name'].strip()
        dob = request.form['dob']
        email = request.form['email'].strip()

        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        # Empty Validation
        if (
            full_name == "" or
            dob == "" or
            email == "" or
            glucose == "" or
            haemoglobin == "" or
            cholesterol == ""
        ):
            return "All fields are required"

        # Email Validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, email):
            return "Invalid Email Address"

        # Date Validation
        try:

            dob_date = datetime.strptime(
                dob,
                '%Y-%m-%d'
            ).date()

            if dob_date > datetime.today().date():
                return "Date of Birth cannot be future date"

        except ValueError:

            return "Invalid Date Format"

        # Numeric Validation
        try:

            glucose = float(glucose)
            haemoglobin = float(haemoglobin)
            cholesterol = float(cholesterol)

        except ValueError:

            return "Blood test values must be numeric"

        # Negative Validation
        if (
            glucose < 0 or
            haemoglobin < 0 or
            cholesterol < 0
        ):
            return "Blood values cannot be negative"

        # AI Prediction
        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        # Database Insert
        try:

            cursor = db.cursor()

            query = """
            INSERT INTO patients
            (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )

            cursor.execute(query, values)

            db.commit()

            cursor.close()

            return redirect('/')

        except Exception as e:

            return "Database Error: " + str(e)

    return render_template('add_patient.html')

# =========================
# Edit Patient
# =========================

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    cursor = db.cursor()

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        try:

            query = """
            UPDATE patients
            SET
                full_name=%s,
                dob=%s,
                email=%s,
                glucose=%s,
                haemoglobin=%s,
                cholesterol=%s,
                remarks=%s
            WHERE id=%s
            """

            values = (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks,
                id
            )

            cursor.execute(query, values)

            db.commit()

            cursor.close()

            return redirect('/')

        except Exception as e:

            return "Database Error: " + str(e)

    cursor.execute(
        "SELECT * FROM patients WHERE id=%s",
        (id,)
    )

    patient = cursor.fetchone()

    cursor.close()

    return render_template(
        'edit_patient.html',
        patient=patient
    )

# =========================
# Delete Patient
# =========================

@app.route('/delete/<int:id>')
def delete_patient(id):

    try:

        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM patients WHERE id=%s",
            (id,)
        )

        db.commit()

        cursor.close()

        return redirect('/')

    except Exception as e:

        return "Database Error: " + str(e)

# =========================
# Run App
# =========================

if __name__ == '__main__':

    app.run(debug=True)
