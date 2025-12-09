# 📘 Quiz API – README

## Overview

This API provides the following features:

* User registration and login via cookie-based authentication
* Automatic quiz generation from YouTube URLs
* Full CRUD functionality for quizzes
* Access restrictions based on user ownership

Authentication is handled via **HttpOnly cookies** (`access_token`, `refresh_token`).

## Authentication

| Token         | Description                            |
| ------------- | -------------------------------------- |
| access_token  | JWT used for authorized requests       |
| refresh_token | Token used to refresh the access token |

## Requirements & Setup

### Prerequisites

To run this project, you need the following installed:

* Python 3.10+
* pip (Python package manager)
* virtualenv (recommended)

### Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

Make sure to configure environment variables for Django settings, database, and any AI service API keys (Gemini, Whisper, etc.).

### Running the Project

1. Apply migrations:

```bash
python manage.py migrate
```

2. Start the development server:

```bash
python manage.py runserver
```

3. API will be available at `http://127.0.0.1:8000/`

# Endpoints

## Auth Endpoints

### POST /api/register/

Registers a new user.
**Request Body**

```json
{
  "username": "your_username",
  "password": "your_password",
  "confirmed_password": "your_confirmed_password",
  "email": "your_email@example.com"
}
```

**Status Codes**

* 201 – User created successfully
* 400 – Invalid data
* 500 – Internal server error

---

### POST /api/login/

Logs in the user and sets auth cookies.
**Request Body**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Status Codes**

* 200 – Login successful
* 401 – Invalid credentials
* 500 – Internal server error

---

### POST /api/logout/

Logs out the user and invalidates tokens.
**Request Body**

```json
{}
```

**Status Codes**

* 200 – Logout successful
* 401 – Not authenticated
* 500 – Internal server error

---

### POST /api/token/refresh/

Refreshes the access token using the refresh token.
**Request Body**

```json
{}
```

**Status Codes**

* 200 – Token refreshed successfully
* 401 – Refresh token invalid or missing
* 500 – Internal server error

---

## Quiz Endpoints

### POST /api/createQuiz/

Creates a quiz based on a YouTube URL.
**Request Body**

```json
{
  "url": "https://www.youtube.com/watch?v=example"
}
```

**Status Codes**

* 201 – Quiz created successfully
* 400 – Invalid URL or data
* 401 – Not authenticated
* 500 – Internal server error

---

### GET /api/quizzes/

Retrieves all quizzes of the authenticated user.
**Status Codes**

* 200 – Success
* 401 – Not authenticated
* 500 – Internal server error

---

### GET /api/quizzes/{id}/

Retrieves a specific quiz.
**URL Parameter**

* `id` – ID of the quiz
  **Status Codes**
* 200 – Success
* 401 – Not authenticated
* 403 – Access denied
* 404 – Quiz not found
* 500 – Internal server error

---

### PATCH /api/quizzes/{id}/

Partially updates a quiz.
**Request Body Example**

```json
{
  "title": "New Title"
}
```

**Status Codes**

* 200 – Updated successfully
* 400 – Invalid data
* 401 – Not authenticated
* 403 – Access denied
* 404 – Quiz not found
* 500 – Internal server error

---

### DELETE /api/quizzes/{id}/

Deletes a quiz permanently.
**Status Codes**

* 204 – Successfully deleted
* 401 – Not authenticated
* 403 – Access denied
* 404 – Quiz not found
* 500 – Internal server error

---

## Error Codes

* 200 – Success
* 201 – Resource created
* 204 – Successfully deleted
* 400 – Invalid data
* 401 – Not authenticated
* 403 – Access denied
* 404 – Not found
* 500 – Internal server error

---

## Rate Limits

This API has **no rate limits**.

---


