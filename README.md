# Health Prediction System

## Project Overview

The Health Prediction System is a Flask-based web application that allows users to manage patient blood test records and generate AI-powered health risk predictions using an external AI API.

The system performs CRUD operations (Create, Read, Update, Delete), validates patient data, stores records in a MySQL database, and integrates with the OpenRouter AI API to generate medical remarks based on blood test values.

---

# Features

* Add patient records
* View all patient records
* Edit patient information
* Delete patient records
* AI-generated health prediction remarks
* MySQL database integration
* Input validation
* Environment variable security using `.env`
* Responsive HTML/CSS frontend

---

# Technologies Used

## Frontend

* HTML5
* CSS3

## Backend

* Python Flask

## Database

* MySQL

## AI API

* OpenRouter API

## Python Libraries

* Flask
* PyMySQL
* Requests
* Python-dotenv

---

# Input Validation Implemented

The application performs the following validations:

* Valid email format validation
* Date of birth cannot be a future date
* Blood test values must be numeric
* Blood test values cannot be negative
* Empty field validation

---

# AI Prediction

The application integrates with the OpenRouter AI API to generate possible health risk predictions based on:

* Glucose
* Haemoglobin
* Cholesterol

Example AI-generated remark:

> Possible diabetes risk with elevated cholesterol and mild anemia indicators.

---

# Project Structure

```text
health-predictor/
│
├── app.py
├── ai_predict.py
├── .env
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── add_patient.html
│   ├── edit_patient.html
```

---

# Database Setup

## Create Database

```sql
CREATE DATABASE health_prediction;
```

## Create Table

```sql
USE health_prediction;

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    dob DATE,
    email VARCHAR(100),
    glucose FLOAT,
    haemoglobin FLOAT,
    cholesterol FLOAT,
    remarks TEXT
);
```

---

# Environment Variables

Create a `.env` file in the project root folder.

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=health_prediction

OPENROUTER_API_KEY=your_api_key
```

---

# Installation Steps

## 1. Clone Repository

```bash
git clone https://github.com/your-username/health-predictor.git
```

## 2. Navigate to Project Folder

```bash
cd health-predictor
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure `.env`

Add your MySQL credentials and OpenRouter API key.

## 5. Run Application

```bash
python app.py
```

---

# Application URL

```text
http://127.0.0.1:5000
```

---

# Sample Test Data

| Full Name    | Glucose | Haemoglobin | Cholesterol |
| ------------ | ------- | ----------- | ----------- |
| John Smith   | 190     | 9.2         | 250         |
| Emma Johnson | 110     | 13.5        | 180         |

---

# Future Improvements

* User authentication
* Search functionality
* Pagination
* Export reports
* Dashboard charts
* Bootstrap responsive UI

---

# Author

Sushmitha M

