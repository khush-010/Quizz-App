Quiz Game Project

Overview:-

  This Django-based quiz game project allows users to participate in quizzes with multiple-choice questions. It includes authentication features, leaderboard functionality, and administrative controls for managing quiz content.

Features:-

  1.Site Access Features:

    Users must be logged in to access quizzes.

    Signup requires username, first name, last name, email address, and password.

    Login requires username and password only.

    Forgot password feature with OTP verification.

    Email verification for new accounts.

  2.Quiz Features:

    All questions are multiple-choice.

    Each question is displayed only once per user.

    Questions are randomly displayed to each user.

    Feedback message after each attempted question on correctness.

  3.Leaderboard Features:

    Leaderboard ranks users based on scores.

    If scores tie, earlier signups rank higher.

    Leaderboard accessible without login.

  4.Administrative Features:

    Only admin can add and manage quiz questions.

    Questions can be added and modified until marked as published.

    Published questions are immutable.

    Admin can search questions by text and filter by publication status.

  5.Technologies Used

    Frontend: HTML, CSS, JavaScript (AJAX for dynamic updates).

    Backend: Django framework.

    Database: PostgreSQL for data storage.
