import csv
from models import Employee
from rule_e import RuleEngine
from rules.exclude_medical import ExcludeMedicalLeaveRule
from rules.exclude_vacation import ExcludeVacation
from rules.exclude_opt_out import ExcludeOptedOutEmployeesRule
from rules.rest_day_eligibility import RestDayEligibilityRule
# from rules.worked_ot_block_holiday import WorkedOTBlockHolidayRule ## TODO reevaluate releavence in real world scenario

def load_employees(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        employees = []
        for row in reader:
            row['rest_days'] = row['rest_days'].split(',')
            row = {k: eval(v) if v in ['True', 'False'] else v for k, v in row.items()}
            employees.append(Employee(**row))
        return employees

def main():
    employees = load_employees("data/employee.csv")

    rules = [
        ExcludeMedicalLeaveRule(),
        ExcludeVacation(),
        ExcludeOptedOutEmployeesRule(),
        RestDayEligibilityRule(),
        # WorkedOTBlockHolidayRule(), ## TODO possibly readd later on.
    ]

    engine = RuleEngine(rules)
    context = {"today": "Tue", 'is_holiday': True} 
    eligible = engine.evaluate_all(employees, context_overrides=context)

    print("Eligible Employees for OT:")
    for emp in eligible:
        print(f"- {emp.name} (ID: {emp.id})")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
