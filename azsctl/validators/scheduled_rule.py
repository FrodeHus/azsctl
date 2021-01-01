import regex
class ScheduledRuleValidator:
    def __init__(self, rule : dict):
        self.rule = rule

    def validate(self):
        if not self._validate_id():
            return False, "id is in the wrong format"
        if not self._validate_name():
            return False, "missing name"
        return True

    def _validate_id(self):
        match = regex.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", self.rule["id"], regex.IGNORECASE)
        if not match:
            return False
        return True
    
    def _validate_name(self):
        name = self.rule["name"]
        if not name:
            return False
        return True