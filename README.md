# 🎓 Student Skill Tracker

A web-based application designed to help students track their skills, monitor learning progress, set personal learning goals, and analyze their development in one place.

## 📌 About the Project

Student Skill Tracker is a Django-based web application developed to help students organize and manage their learning journey.

Students can create an account, add skills, update their progress, set learning goals, and view their progress through an analytics dashboard.

## ✨ Features

- *User Authentication:* Secure registration, login, and logout.
- *Personal Dashboard:* View an overview of learning activities.
- *Skill Management:* Add, update, and delete skills.
- *Progress Tracking:* Monitor skill development.
- *Learning Goals:* Set and manage personal learning goals.
- *Analytics:* View learning progress and activity statistics.
- *User Profiles:* Manage personal profile information.
- *Individual Accounts:* Each student has their own data.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django 5.2 | Web framework |
| MySQL | Database |
| HTML5 | Webpage structure |
| CSS3 | Styling |
| JavaScript | Frontend interactions |
| Bootstrap (if used) | Responsive UI |

## 📂 Project Structure

text
student-skill-tracker/
│
├── manage.py
├── mysql.sql
├── requirements.txt
├── .gitignore
│
├── skill_tracker_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── tracker/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── migrations/
│
└── templates/
    ├── auth/
    └── tracker/


## ⚙️ Installation and Setup

Follow these steps to run the project on your computer.

### 1. Clone the repository

bash
git clone https://github.com/NeevTrivedi/student-skill-tracker.git


### 2. Open the project folder

bash
cd student-skill-tracker


### 3. Create a virtual environment

bash
python -m venv venv


Activate it on Windows:

bash
venv\Scripts\activate


### 4. Install dependencies

bash
pip install -r requirements.txt


### 5. Configure MySQL

- Install and start MySQL Server.
- Create the database configured in settings.py.
- Set the DB_PASSWORD environment variable to your MySQL password.

For Windows PowerShell:

powershell
$env:DB_PASSWORD = Read-Host "Enter your MySQL password"


### 6. Apply migrations

bash
python manage.py migrate


### 7. Run the development server

bash
python manage.py runserver


Open your browser and visit:

text
http://127.0.0.1:8000/


## 🎯 Project Objective

The main objective of this project is to encourage students to develop new skills, maintain consistent learning habits, and keep track of their personal growth.

## 👨‍💻 Developed By

*Student Skill Tracker Project Team*

GitHub Repository: https://github.com/NeevTrivedi/student-skill-tracker

---

This project is developed as part of an academic group project.