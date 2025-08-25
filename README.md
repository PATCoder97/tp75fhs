# TP75 FHS Project

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/tp75_fhs
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API:
- API Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc

## API Endpoints

- `POST /users/` - Create new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user