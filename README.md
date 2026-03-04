# fitness-progress-tracker

A Django-based web application to track workout plans, exercises, workout sessions, and user progress.  
This project allows users to create personalized workout plans, log exercises, track their sessions, and monitor progress over time.

---

## Features

- User registration and authentication
- Create, update, and delete workout plans
- Add exercises to workout plans
- Log workout sessions and mark them as completed
- Track progress with detailed records for each exercise
- Pagination and search for workout plans, exercises, sessions, and progress records
- User-friendly dashboard showing summary statistics

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RodionDem/fitness-progress-tracker.git
   cd fitness-progress-tracker
   
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Apply database migrations:
    ```bash
    python manage.py migrate

5. Create a superuser
    ```bash
   python manage.py createsuperuser

6. Run the development server:
    ```bash
   python manage.py runserver

7. Open your browser at:
   http://127.0.0.1:8000/

---

## Usage

- Register a new user or log in
- Create workout plans and exercises
- Log your workout sessions
- Add progress records for exercises
- View statistics and summaries on your dashboard

---

## Running Tests

- All unit tests are included for models, forms, and views. Run tests with:
    ```bash
    python manage.py test

---

## Project Structure

fitness-progress-tracker/
├─ workouts/               # Main app
│  ├─ models.py            # User, WorkoutPlan, Exercise, WorkoutSession, ProgressRecord
│  ├─ views.py             # All views and class-based views
│  ├─ forms.py             # Forms for CRUD operations
│  ├─ tests/               # Unit tests for models, forms, and views
│  └─ templates/           # HTML templates for dashboard, plans, exercises, sessions, progress
├─ db.sqlite3              # SQLite database
├─ manage.py               # Django management script
├─ requirements.txt        # Python dependencies
└─ README.md               # Project documentation

