class IncidentClassificationReason:
    INACCURATE_DATA = "InaccurateData"
    INCORRECT_ALERT_LOGIC = "IncorrectAlertLogic"
    SUSPICIOUS_ACTIVITY = "SuspiciousActivity"
    SUSPICIOUS_BUT_EXPECTED = "SuspiciousButExcepted"

class IncidentClassification:
    BENIGN_POSITIVE = "BenignPositive"
    FALSE_POSITIVE = "FalsePositive"
    TRUE_POSITIVE = "TruePositive"
    UNDETERMINED = "Undetermined"

class IncidentStatus:
    ACTIVE = "Active"
    CLOSED = "Closed"
    NEW = "New"

class IncidentSeverity:
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"