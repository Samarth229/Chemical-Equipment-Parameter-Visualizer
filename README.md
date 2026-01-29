# Chemical Equipment Parameter Visualizer – Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- Git

---

## Backend Setup (Django)

1. Navigate to backend folder  
2. Create virtual environment  
3. Install dependencies  
4. Run migrations  
5. Create superuser  
6. Start server  

---

## Backend Authentication Credentials

The backend APIs are protected using **Basic Authentication**.

Use the following credentials while accessing APIs from:
- React frontend
- PyQt desktop application
- Browser / Postman

**Username**
Fossee


**Password**
fossee123


⚠️ These credentials are hardcoded **only for demo and academic purposes**.

---

## Creating Superuser (Required)

While running the backend, create a Django superuser using:

python manage.py createsuperuser
Use the same username and password mentioned above:

Username: Fossee
Password: fossee123
Starting Backend Server
python manage.py runserver
Backend will be available at:

http://127.0.0.1:8000/
Web Frontend Setup (React)
Navigate to frontend folder

Install dependencies

Start development server

npm install
npm start
Web app runs at:

http://localhost:3000
Desktop Application Setup (PyQt)
Install required Python libraries

Run the desktop app

pip install pyqt5 matplotlib requests
python main.py
Notes
Both React and PyQt applications automatically attach authentication headers.

Uploading CSV without valid credentials will fail.

PDF reports can be downloaded only for authenticated users.


