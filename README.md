# Student Attendance Management System

A Django application for managing students, teachers, classes, subjects, attendance records, and attendance detail entries.

## Features

- Teacher and student account creation and authentication
- Class, subject, and teacher management
- Attendance scheduling and recording
- Attendance detail editing and deletion
- Admin interface support via Django admin

## Setup

1. Create a Python virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   # Windows CMD
   .\venv\Scripts\activate.bat
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Notes

- The project uses SQLite by default (`db.sqlite3`).
- In production, set `DEBUG = False` and provide secure secret keys.
- `requirements.txt` contains required Python dependencies.
