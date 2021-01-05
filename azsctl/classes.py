import datetime
import uuid
import dateutil
from typing import List
from enum import Enum


class AlertRuleKind(Enum):
    FUSION = "Fusion"
    MICROSOFT_SECURITY_INCIDENT_CREATION = "MicrosoftSecurityIncidentCreation"
    SCHEDULED = "Scheduled"


class IncidentClassificationReason(Enum):
    INACCURATE_DATA = "InaccurateData"
    INCORRECT_ALERT_LOGIC = "IncorrectAlertLogic"
    SUSPICIOUS_ACTIVITY = "SuspiciousActivity"
    SUSPICIOUS_BUT_EXPECTED = "SuspiciousButExcepted"


class IncidentClassification(Enum):
    BENIGN_POSITIVE = "BenignPositive"
    FALSE_POSITIVE = "FalsePositive"
    TRUE_POSITIVE = "TruePositive"
    UNDETERMINED = "Undetermined"


class IncidentStatus(Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"
    NEW = "New"


class IncidentSeverity(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"


class AlertSeverity(Enum):
    HIGH = "High"
    INFORMATIONAL = "Informational"
    LOW = "Low"
    MEDIUM = "Medium"


class TemplateStatus(Enum):
    AVAILABLE = "Available"
    INSTALLED = "Installed"
    NOT_AVAILABLE = "NotAvailable"


class TriggerOperator(Enum):
    EQUAL = "Equal"
    GREATER_THAN = "GreaterThan"
    LESS_THAN = "LessThan"
    NOT_EQUAL = "NotEqual"

class ScheduledAlertRule:
    def __init__(self, values: dict = None):
        self.kind = AlertRuleKind.SCHEDULED
        self.etag = None
        self.properties = {}
        if values:
            self.__dict__ = values

    @staticmethod
    def from_template(template):
        rule = ScheduledAlertRule()
        rule.name = uuid.uuid4()
        rule.alert_rule_template_name = template.name
        rule.display_name = template.display_name
        rule.enabled = True
        return rule

    @property
    def alert_rule_template_name(self):
        return self.properties["alertRuleTemplateName"]
    
    @alert_rule_template_name.setter
    def alert_rule_template_name(self, value):
        self.properties["alertRuleTemplateName"] = value

    @property
    def display_name(self):
        return self.properties["displayName"]

    @display_name.setter
    def display_name(self, value):
        self.properties["displayName"] = value

    @property
    def description(self):
        return self.properties["description"]

    @description.setter
    def description(self, value):
        self.properties["description"] = value

    @property
    def query(self):
        return self.properties["query"]

    @query.setter
    def query(self, value):
        self.properties["query"] = value

    @property
    def query_period(self):
        return self.properties["queryPeriod"]

    @query_period.setter
    def query_period(self, value):
        self.properties["queryPeriod"] = value

    @property
    def query_frequency(self):
        return self.properties["queryFrequency"]

    @query_frequency.setter
    def query_frequency(self, value):
        self.properties["queryFrequency"] = value

    @property
    def severity(self):
        return self.properties["severity"]

    @severity.setter
    def severity(self, value: AlertSeverity):
        self.properties["severity"] = value

    @property
    def trigger_operator(self) -> TriggerOperator:
        return self.properties["triggerOperator"]

    @trigger_operator.setter
    def trigger_operator(self, value: TriggerOperator):
        self.properties["triggerOperator"] = value

    @property
    def trigger_threshold(self):
        return self.properties["triggerThreshold"]

    @trigger_threshold.setter
    def trigger_threshold(self, value: int):
        self.properties["triggerThreshold"] = value

    @property
    def tactics(self) -> List[str]:
        return self.properties["tactics"]

    @tactics.setter
    def tactics(self, value: List[str]):
        self.properties["tactics"] = value

class ScheduledAlertRuleTemplate(ScheduledAlertRule):
    def __init__(self, values: dict = None):
        super().__init__(values)
        self.id = None
        self.name = None
        self.type = "Microsoft.SecurityInsights/AlertRuleTemplates"
        self.properties = {}

        if values:
            self.__dict__ = values

    @staticmethod
    def from_yaml_template(values: dict):
        def read_value(values: dict, key: str):
            if key in values:
                return values[key]
            return None

        def parse_operator(value: str) -> TriggerOperator:
            if value == "gt":
                return TriggerOperator.GREATER_THAN
            if value == "lt":
                return TriggerOperator.LESS_THAN
            if value == "ne":
                return TriggerOperator.NOT_EQUAL
            if value == "eq":
                return TriggerOperator.NOT_EQUAL
            return value

        template = ScheduledAlertRuleTemplate()
        template_id = read_value(values, "id")
        from azsctl import current_config
        _, workspace_id = current_config.get_workspace()
        template.id = f"{workspace_id}/alertRules/{template_id}"
        template.display_name = read_value(values, "name")
        template.name = template_id
        template.description = read_value(values, "description")
        template.severity = read_value(values, "severity")
        template.query_frequency = read_value(values, "queryFrequency")
        template.query = read_value(values, "query")
        template.query_period = read_value(values, "queryPeriod")
        template.tactics = read_value(values, "tactics")
        template.status = read_value(values, "status")
        template.trigger_operator = parse_operator(
            read_value(values, "triggerOperator")
        )
        return template

    @property
    def created_date(self):
        return dateutil.parser.parse(self.properties["createdDateUTC"])

    @created_date.setter
    def created_date(self, value: datetime.datetime):
        self.properties["createdDateUTC"] = value


    @property
    def status(self):
        return self.properties["status"]

    @status.setter
    def status(self, value: TemplateStatus):
        self.properties["status"] = value

    @property
    def alert_rules_created_by_template(self):
        return self.properties["alertRulesCreatedByTemplateCount"]

    @alert_rules_created_by_template.setter
    def alert_rules_created_by_template(self, value: int):
        self.properties["alertRulesCreatedByTemplateCount"] = value
