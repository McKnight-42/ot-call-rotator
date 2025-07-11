from rules.base_rule import BaseRule, RuleResult

class ExcludeOptedOutEmployeesRule(BaseRule):
    def evaluate(self, context):
        employee = context["employee"]
        if employee.exclude_from_ot:
            return RuleResult(False, "Employee opted out of OT", self.name)
        return RuleResult(True, "Eligible", self.name)
