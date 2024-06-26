Quiz Game Project
Overview
This Django-based quiz game project allows users to participate in quizzes with multiple-choice questions. It includes authentication features, leaderboard functionality, and administrative controls for managing quiz content.

Features
Site Access Features:
Users must be logged in to access quizzes.
Signup requires username, first name, last name, email address, and password.
Login requires username and password only.
Forgot password feature with OTP verification.
Email verification for new accounts.
Quiz Features:
All questions are multiple-choice.
Each question is displayed only once per user.
Questions are randomly displayed to each user.
Accidental page refresh or navigation marks the current question as attempted.
Feedback message after each attempted question on correctness.
Leaderboard Features:
Leaderboard ranks users based on scores.
If scores tie, earlier signups rank higher.
Leaderboard accessible without login.
Administrative Features:
Only admin can add and manage quiz questions.
Questions can be added and modified until marked as published.
Published questions are immutable.
Admin can search questions by text and filter by publication status.
Technologies Used
Frontend: HTML, CSS, JavaScript (AJAX for dynamic updates).
Backend: Django framework.
Database: SQLite/PostgreSQL for data storage.
