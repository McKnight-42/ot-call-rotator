from rules.base_rule import BaseRule, RuleResult

class ExcludeVacation(BaseRule):
    def evaluate(self, context):
        employee = context["employee"]
        if employee.on_vacation:
            return RuleResult(False, "On Vacation", self.name)
        return RuleResult(True, "Eligible", self.name)