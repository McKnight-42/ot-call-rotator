import unittest
from models import Employee
from rules.exclude_vacation import ExcludeVacation
from rules.exclude_medical import ExcludeMedicalLeaveRule
from rules.exclude_opt_out import ExcludeOptedOutEmployeesRule
from rules.rest_day_eligibility import RestDayEligibilityRule

class TestBasicRules(unittest.TestCase):

    def setUp(self):
        self.emp_vacation = Employee(
            id=1,
            name="On Vacation",
            rest_days=["Tue"],
            on_medical_leave=False,
            on_vacation=True,
            exclude_from_ot=False,
            shift="1st",
            worked_ot_yesterday=False,
            role_type="signal",
        )
        self.emp_medical = Employee(
            id=2,
            name="On Medical",
            rest_days=["Tue"],
            on_medical_leave=True,
            on_vacation=False,
            exclude_from_ot=False,
            shift="2nd",
            worked_ot_yesterday=False,
            role_type="welder",
        )
        self.emp_optout = Employee(
            id=3,
            name="Opted Out",
            rest_days=["Tue"],
            on_medical_leave=False,
            on_vacation=False,
            exclude_from_ot=True,
            shift="3rd",
            worked_ot_yesterday=False,
            role_type="signal",
        )
        self.emp_okay = Employee(
            id=4,
            name="Eligible",
            rest_days=["Tue"],
            on_medical_leave=False,
            on_vacation=False,
            exclude_from_ot=False,
            shift="1st",
            worked_ot_yesterday=False,
            role_type="signal",
        )


    def test_exclude_vacation(self):
        rule = ExcludeVacation()
        self.assertFalse(rule.evaluate({"employee": self.emp_vacation}).eligible)
        self.assertTrue(rule.evaluate({"employee": self.emp_okay}).eligible)

    def test_exclude_medical(self):
        rule = ExcludeMedicalLeaveRule()
        self.assertFalse(rule.evaluate({"employee": self.emp_medical}).eligible)
        self.assertTrue(rule.evaluate({"employee": self.emp_okay}).eligible)

    def test_exclude_opt_out(self):
        rule = ExcludeOptedOutEmployeesRule()
        self.assertFalse(rule.evaluate({"employee": self.emp_optout}).eligible)
        self.assertTrue(rule.evaluate({"employee": self.emp_okay}).eligible)

    def test_rest_day_eligibility(self):
        rule = RestDayEligibilityRule()
        # Test today is rest day
        self.assertTrue(rule.evaluate({"employee": self.emp_okay, "today": "Tue"}).eligible)
        # Test today is not rest day
        self.assertFalse(rule.evaluate({"employee": self.emp_okay, "today": "Mon"}).eligible)


if __name__ == "__main__":
    unittest.main()
