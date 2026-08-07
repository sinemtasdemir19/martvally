# Martvally

**AI-Powered Project Planning & Lead Management Platform**

Martvally is a full-stack AI-powered web application that helps users receive intelligent project guidance through an AI assistant while allowing businesses to collect and manage customer leads through a dedicated dashboard.

The project was developed using a modular architecture based on the **Separation of Concerns (SoC)** principle with **Python, Flask, SQLite, Groq API, Render, and Wix Studio**.

---

## Features

- AI-powered project planning assistant
- Conversation history support
- Lead collection system
- Business management dashboard
- RESTful API architecture
- Live deployment with Render
- Wix Studio frontend integration

---

## Technologies

### Backend
- Python
- Flask
- SQLite
- Flask-CORS
- Requests
- python-dotenv
- Gunicorn

### AI
- Groq API
- Llama-3.1-8B-Instant

### Frontend
- Wix Studio
- Wix Velo
- wix-fetch

### Deployment
- GitHub
- Render

---

## Project Structure

```text
martvally/
│
├── run.py
├── config.py
├── requirements.txt
├── .gitignore
│
└── app/
    ├── __init__.py
    ├── database.py
    ├── routes.py
    ├── templates/
    │   ├── index.html
    │   └── dashboard.html
    │
    └── services/
        ├── __init__.py
        └── ai_service.py
```

---

## Architecture

The project follows the **Separation of Concerns** principle.

| Layer | Responsibility |
|--------|---------------|
| config.py | Application configuration |
| database.py | SQLite operations |
| ai_service.py | AI communication |
| routes.py | REST API endpoints |
| __init__.py | Flask application factory |
| run.py | Application entry point |

---

## API Endpoints

### Health Check

```
GET /health
```

### AI Chat

```
POST /api/chat
```

Example request

```json
{
  "message": "How can I plan my project?",
  "history": []
}
```

---

### Save Lead

```
POST /api/leads
```

Example request

```json
{
  "name": "John Doe",
  "phone": "+1 555 123 4567",
  "message": "I need help planning my project."
}
```

---

### Get Leads

```
GET /api/leads
```

---

## Local Installation

Clone the repository

```bash
git clone https://github.com/sinemtasdemir19/martvally.git
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=martvally.db
```

Run the application

```bash
python run.py
```

---

## Live Demo

### Wix Frontend

https://sinemt.wixstudio.com/martvally


### Render Backend

https://martvally.onrender.com

Health Check

https://martvally.onrender.com/health

---

## Workflow

```
User
   │
   ▼
Wix Studio
   │
   ▼
Flask REST API
   │
   ├── Groq AI
   └── SQLite Database
```

---

## Security

- API keys are stored in `.env`
- Parameterized SQL queries prevent SQL Injection
- CORS is configured for frontend communication
- Exception handling is implemented throughout the application
