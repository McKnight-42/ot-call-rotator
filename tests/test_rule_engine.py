import unittest
from models import Employee
from rules.exclude_vacation import ExcludeVacation
from rules.exclude_medical import ExcludeMedicalLeaveRule
from rules.exclude_opt_out import ExcludeOptedOutEmployeesRule
from rules.rest_day_eligibility import RestDayEligibilityRule
from rule_e import RuleEngine

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        self.employees = [
            Employee(id=1, name="A", rest_days=["Tue"], on_medical_leave=False, on_vacation=False, exclude_from_ot=False, shift="1st", worked_ot_yesterday=False, role_type="signal"),
            Employee(id=2, name="B", rest_days=["Wed"], on_medical_leave=True, on_vacation=False, exclude_from_ot=False, shift="2nd", worked_ot_yesterday=False, role_type="welder"),
            Employee(id=3, name="C", rest_days=["Tue"], on_medical_leave=False, on_vacation=True, exclude_from_ot=False, shift="3rd", worked_ot_yesterday=False, role_type="signal"),
            Employee(id=4, name="D", rest_days=["Tue"], on_medical_leave=False, on_vacation=False, exclude_from_ot=True, shift="3rd", worked_ot_yesterday=False, role_type="signal"),
        ]
        self.rules = [
            ExcludeMedicalLeaveRule(),
            ExcludeVacation(),
            ExcludeOptedOutEmployeesRule(),
            RestDayEligibilityRule(),
        ]
        self.engine = RuleEngine(self.rules)

    def test_engine_filters_correctly(self):
        eligible = self.engine.evaluate_all(self.employees, context_overrides={"today": "Tue"})
        eligible_names = {e.name for e in eligible}
        self.assertIn("A", eligible_names)
        self.assertNotIn("B", eligible_names)
        self.assertNotIn("C", eligible_names)
        self.assertNotIn("D", eligible_names)
        self.assertEqual(len(eligible), 1)

if __name__ == "__main__":
    unittest.main()
