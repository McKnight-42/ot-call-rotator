class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def evaluate_all(self, employees, context_overrides=None):
        eligible = []

        for emp in employees:
            context = {"employee": emp, **(context_overrides or {})}
            results = [rule.evaluate(context) for rule in self.rules]
            if all(r.eligible for r in results):
                eligible.append(emp)
        return eligible
