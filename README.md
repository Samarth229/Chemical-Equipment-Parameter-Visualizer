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

## Creating Superuser (Required for Authentication)

This project uses **Basic Authentication**.  
You must create a Django superuser to access protected APIs.

### Step 1: Start Backend Environment
Activate the virtual environment and navigate to the backend directory:

```bash
cd foss_backend
venv\Scripts\activate
Step 2: Create Superuser
Run the following command:

python manage.py createsuperuser
Use the credentials below (important – frontend uses the same):

Username: Fossee

Password: fossee123

Starting Backend Server
After creating the superuser, start the Django development server:

python manage.py runserver
Backend will be available at:

http://127.0.0.1:8000/
Web Frontend Setup (React)
Step 1: Navigate to frontend folder
cd foss_frontend
Step 2: Install dependencies
npm install
Step 3: Start development server
npm start
Web application will run at:

http://localhost:3000
⚠️ The React app automatically sends authentication headers.
Uploading CSV without valid credentials will fail.

Desktop Application Setup (PyQt)
Step 1: Install required Python libraries
pip install pyqt5 matplotlib requests
Step 2: Run the desktop application
python main.py
⚠️ The PyQt application also automatically attaches authentication headers.

Authentication Notes
All CSV uploads, history access, and PDF downloads are protected.

Invalid credentials will result in 401 Unauthorized.

PDF reports can be downloaded only by authenticated users.
