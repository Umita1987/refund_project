# Refund Request Management System

A simple Django-based application for managing refund requests, including client-side and server-side IBAN validation, user authentication, REST API, and email notifications.

## Features
- Creating refund requests with IBAN validation via external API (cached validation)
- List, view, update, and delete refund requests (CRUD)
- REST API access with JWT authentication
- Email notifications upon refund status changes
- Bootstrap-based responsive UI

## Technology Stack
- Python
- Django
- Django REST Framework
- PostgreSQL
- Bootstrap 5
- JWT authentication (Simple JWT)
- External IBAN validation API (API Ninjas)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Umita1987/refund_project.git
cd refund_project
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Change .envexample to your .env.  Set environment variables or update `settings.py` with your credentials (API keys, SMTP credentials). 

5. Run migrations:

```bash
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

## Testing

Run tests using Django's built-in testing system:

```bash
python manage.py test refunds
```

## API

API endpoints documentation:

- List/Create Refund Requests: `/api/refunds/`
- Refund Request details: `/api/refunds/<id>/`

Use JWT tokens for authentication.

