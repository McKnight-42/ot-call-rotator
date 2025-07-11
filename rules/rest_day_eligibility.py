from rules.base_rule import BaseRule, RuleResult
import datetime


class RestDayEligibilityRule(BaseRule):
    def evaluate(self, context):
        employee = context["employee"]
        today = context.get("today") or datetime.date.today().strftime("%a")
        rest_days = [d.strip()[:3] for d in employee.rest_days]

        if today in rest_days:
            return RuleResult(True, "Rest day OT allowed", self.name)
        return RuleResult(False, "Not rest day", self.name)
