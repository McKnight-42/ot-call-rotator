from dataclasses import dataclass

@dataclass
class RuleResult:
    eligible: bool
    reason: str
    rule_name: str

class BaseRule:
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    def evaluate(self, context) -> RuleResult:
        raise NotImplementedError
