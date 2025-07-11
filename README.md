# 🛠️ OT Call Rotator

A rules-based scheduling tool for determining employee eligibility for overtime (OT) and holiday shifts based on configurable business logic. Built to support both CLI and API workflows, with plans for an interactive frontend.

---

## 🚀 Features

- Rules engine to evaluate employee eligibility
- CLI tool for local batch evaluations
- FastAPI web service for real-time access
- CSV-based input with context flags (`today`, `is_holiday`)
- Modular rule system for flexible business logic
- Unit + integration test coverage

---

## 📦 Project Structure

ot-call-rotator/
├── data/ # Sample CSVs
├── rules/ # Modular rule files
├── api/ # FastAPI app and endpoints
│ └── tests/ # API-level test cases
├── tests/ # CLI + rule engine tests
├── models.py # Pydantic Employee model
├── rule_e.py # RuleEngine core
├── main.py # CLI entry point
└── requirements.txt # Dependencies

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/yourname/ot-call-rotator.git
cd ot-call-rotator

# (Optional) Create and activate a virtualenv
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## 🖥️ CLI Usage
```
python main.py
```

## 🌐 API Usage (FastAPI)

Start the server
```
uvicorn api.app:app --reload
```

Test health check
```
curl http://localhost:8000/ping
```

Evaluate CSV (upload endpoint)
```
curl -X POST "http://localhost:8000/evaluate/csv?today=Tue&is_holiday=false" \
  -F "file=@data/employee.csv"
```

API Docs
Swagger: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc


## 🧪 Running Tests
CLI tests
```
python -m unittest discover -s tests -v
```

API tests
```
python -m unittest discover -s api/tests -v
```

## 📅 Roadmap
 CLI rules engine

 FastAPI with CSV input

 Add JSON input support

 Build React + TypeScript frontend

 GUI rule configurator for non-technical users

 Persistent database support (PostgreSQL)

## 🧭 System Architecture Overview

```mermaid
                       ┌────────────────────────┐
                        │   data/employee.csv    │
                        └────────────┬───────────┘
                                     │
                          ┌──────────▼──────────┐
                          │  Pydantic Employee  │
                          │   Model Parsing     │
                          └──────────┬──────────┘
                                     │
                            (shared in both)
                                     ▼
                          ┌────────────────────┐
                          │   RuleEngine.py    │
                          │  Applies Rules:     │
                          │  - Vacation         │
                          │  - Medical Leave    │
                          │  - Rest Day Logic   │
                          └──────────┬──────────┘
                                     │
                    ┌─────────────────────────────────┐
                    │                                 │
       CLI Mode     ▼                                 ▼     API Mode
┌──────────────┐       ┌────────────────────┐    ┌──────────────────────────┐
│ main.py CLI  │──────▶│  Prints to Console │    │    FastAPI: /evaluate    │
└──────────────┘       └────────────────────┘    └──────┬───────────────────┘
                                                        │
                         ┌──────────────────────────────▼────────────────────────────┐
                         │ Swagger UI /curl /Postman ───── CSV Upload or JSON Input  │
                         └───────────────────────────────────────────────────────────┘
                                                        │
                                           ┌────────────▼────────────┐
                                           │  JSON Response of       │
                                           │  Eligible Employees     │
                                           └────────────┬────────────┘
                                                        │
                                          (Coming soon) ▼
                                        ┌────────────────────┐
                                        │ React + Tailwind   │
                                        │ Frontend Upload UI │
                                        └────────────────────┘
```
