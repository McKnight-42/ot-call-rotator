import unittest
from models import Employee
from rules.exclude_vacation import ExcludeVacation
from rules.exclude_medical import ExcludeMedicalLeaveRule
from rules.exclude_opt_out import ExcludeOptedOutEmployeesRule
from rules.rest_day_eligibility import RestDayEligibilityRule

class TestRulesEdgeCases(unittest.TestCase):

    def setUp(self):
        self.emp_empty_rest = Employee(
            id=10,
            name="Empty Rest",
            rest_days=[],
            on_medical_leave=False,
            on_vacation=False,
            exclude_from_ot=False,
            shift="1st",
            worked_ot_yesterday=False,
            role_type="signal",
        )
        self.emp_conflict = Employee(
            id=11,
            name="Conflicted",
            rest_days=["Tue"],
            on_medical_leave=False,
            on_vacation=True,
            exclude_from_ot=True,
            shift="1st",
            worked_ot_yesterday=False,
            role_type="signal",
        )
        self.emp_bad_rest_format = Employee(
            id=12,
            name="Bad Rest Format",
            rest_days=["Tuesday "],  # extra space and full name
            on_medical_leave=False,
            on_vacation=False,
            exclude_from_ot=False,
            shift="2nd",
            worked_ot_yesterday=False,
            role_type="welder",
        )

    def test_empty_rest_days(self):
        rule = RestDayEligibilityRule()
        # Should not be eligible on any day since no rest days defined
        self.assertFalse(rule.evaluate({"employee": self.emp_empty_rest, "today": "Tue"}).eligible)
        self.assertFalse(rule.evaluate({"employee": self.emp_empty_rest, "today": "Mon"}).eligible)

    def test_conflicting_flags(self):
        vac_rule = ExcludeVacation()
        optout_rule = ExcludeOptedOutEmployeesRule()

        self.assertFalse(vac_rule.evaluate({"employee": self.emp_conflict}).eligible)
        self.assertFalse(optout_rule.evaluate({"employee": self.emp_conflict}).eligible)

    def test_rest_day_full_name_and_whitespace(self):
        rule = RestDayEligibilityRule()
        # Normalize should trim whitespace and take first 3 chars
        self.assertTrue(rule.evaluate({"employee": self.emp_bad_rest_format, "today": "Tue"}).eligible)
        self.assertFalse(rule.evaluate({"employee": self.emp_bad_rest_format, "today": "Mon"}).eligible)

if __name__ == "__main__":
    unittest.main()
