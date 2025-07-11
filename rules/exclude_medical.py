from rules.base_rule import BaseRule, RuleResult

class ExcludeMedicalLeaveRule(BaseRule):
    def evaluate(self, context):
        employee = context["employee"]
        if employee.on_medical_leave:
            return RuleResult(False, "On medical leave", self.name)
        return RuleResult(True, "Eligible", self.name)
