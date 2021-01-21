import regex
from azsentinel.classes import ScheduledAlertRuleTemplate
class ScheduledRuleValidator:
    def __init__(self, rule : ScheduledAlertRuleTemplate):
        self.rule = rule

    def validate(self):
        if not self._validate_name():
            return False, "id is in the wrong format"
        if not self._validate_display_name():
            return False, "missing name"
        return True, None

    def _validate_name(self):
        match = regex.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", self.rule.name, regex.IGNORECASE)
        if not match:
            return False
        return True
    
    def _validate_display_name(self):
        if not self.rule.display_name:
            return False
        return True