# SplitTrail

A bill-splitting app for camping trips. Splitwise clone built with FastAPI, MySQL, and Vue.

## Stack
- Backend: Python + FastAPI
- Database: MySQL 8.0 (Docker)
- Frontend: Vue (coming soon)
- CI/CD: GitHub Actions (coming soon)

## Prerequisites
- Python 3.x
- Docker + docker-compose
- Node.js (for frontend, coming soon)

## Getting started

### 1. Clone the repo
git clone https://github.com/windsleigh/split_trail.git
cd split_trail

### 2. Create the virtual environment
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

### 3. Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your values

### 4. Start everything
./scripts/dev_start.sh

### 5. Open the API docs
http://localhost:8001/docs

## Stopping the dev environment
./scripts/dev_stop.sh

## Project structure
split_trail/
├── backend/
│   ├── app/
│   │   ├── models/       # SQLAlchemy database models
│   │   ├── routes/       # FastAPI route handlers
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Business logic
│   │   ├── config.py     # Environment config
│   │   ├── database.py   # DB connection and session
│   │   └── main.py       # App entry point
│   └── requirements.txt
├── scripts/
│   ├── dev_start.sh      # Start everything
│   └── dev_stop.sh       # Stop everything
└── docker-compose.yml