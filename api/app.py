from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import csv
from io import StringIO
from typing import List
from models import Employee
from rule_e import RuleEngine
from rules.exclude_medical import ExcludeMedicalLeaveRule
from rules.exclude_vacation import ExcludeVacation
from rules.exclude_opt_out import ExcludeOptedOutEmployeesRule
from rules.rest_day_eligibility import RestDayEligibilityRule

app = FastAPI(title="OT Call Rotator API")

rules = [
    ExcludeMedicalLeaveRule(),
    ExcludeVacation(),
    ExcludeOptedOutEmployeesRule(),
    RestDayEligibilityRule(),
]

engine = RuleEngine(rules)

def parse_csv_to_employees(file_contents: str) -> List[Employee]:
    reader = csv.DictReader(StringIO(file_contents))
    employees = []
    for row in reader:
        row['rest_days'] = row['rest_days'].split(',')
        row = {k: (v == 'True' if v in ['True', 'False'] else v) for k, v in row.items()}
        employees.append(Employee(**row))
    return employees

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/evaluate/csv")
async def evaluate_csv(file: UploadFile = File(...), today: str = "Tue", is_holiday: bool = False):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    contents = await file.read()
    try:
        employees = parse_csv_to_employees(contents.decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {e}")

    context = {"today": today, "is_holiday": is_holiday}
    eligible = engine.evaluate_all(employees, context_overrides=context)

    result = [{"id": e.id, "name": e.name, "shift": e.shift} for e in eligible]
    return JSONResponse(content={"eligible_employees": result})
