from rules.base_rule import BaseRule, RuleResult

class WorkedOTBlockHolidayRule(BaseRule):
    def evaluate(self, context):
        employee = context["employee"]
        is_holiday = context.get("is_holiday", False)

        if is_holiday and employee.worked_ot_yesterday:
            return RuleResult(False, "Worked OT yesterday — blocked from holiday", self.name)
        return RuleResult(True, "Eligible", self.name)
