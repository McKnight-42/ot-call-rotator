import unittest
from pydantic import BaseModel
from rules.base_rule import BaseRule, RuleResult
from models import Employee

class HolidayRule(BaseRule):
    def evaluate(self, context):
        is_holiday = context.get("is_holiday", False)
        employee = context["employee"]
        if is_holiday:
            return RuleResult(True, "Holiday OT - open eligibility", self.name)
        else:
            if employee.exclude_from_ot:
                return RuleResult(False, "Excluded from OT", self.name)
            return RuleResult(True, "Eligible", self.name)

class TestHolidayRule(unittest.TestCase):

    def setUp(self):
        self.emp_optout = Employee(
            id=1,
            name="Opted Out",
            rest_days=["Tue"],
            on_medical_leave=False,
            on_vacation=False,
            exclude_from_ot=True,
            shift="1st",
            worked_ot_yesterday=False,
            role_type="signal",
        )
        self.emp_okay = Employee(
            id=2,
            name="Eligible",
            rest_days=["Tue"],
            on_medical_leave=False,
            on_vacation=False,
            exclude_from_ot=False,
            shift="1st",
            worked_ot_yesterday=False,
            role_type="signal",
        )

    def test_holiday_true(self):
        rule = HolidayRule()
        # On holiday, everyone eligible regardless of opt-out
        self.assertTrue(rule.evaluate({"employee": self.emp_optout, "is_holiday": True}).eligible)
        self.assertTrue(rule.evaluate({"employee": self.emp_okay, "is_holiday": True}).eligible)

    def test_holiday_false(self):
        rule = HolidayRule()
        # Not holiday, respect opt-out
        self.assertFalse(rule.evaluate({"employee": self.emp_optout, "is_holiday": False}).eligible)
        self.assertTrue(rule.evaluate({"employee": self.emp_okay, "is_holiday": False}).eligible)

if __name__ == "__main__":
    unittest.main()
