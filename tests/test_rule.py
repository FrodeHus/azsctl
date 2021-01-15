from azsentinel.classes import ScheduledAlertRuleTemplate
import unittest
from unittest import mock
import yaml
from azsentinel.validators import ScheduledRuleValidator

test_rule = """
id: e1ce0eab-10d1-4aae-863f-9a383345ba88
name: SSH - Potential Brute Force
description: |
  'Identifies an IP address that had 15 failed attempts to sign in via SSH in a 4 hour block during a 24 hour time period.'
severity: Low
requiredDataConnectors:
  - connectorId: Syslog
    dataTypes:
      - Syslog
queryFrequency: 1d
queryPeriod: 1d
triggerOperator: gt
triggerThreshold: 0
tactics:
  - CredentialAccess
relevantTechniques:
  - T1110
query: |

  let timeframe = 1d;
  let threshold = 15;
  Syslog
  | where TimeGenerated >= ago(timeframe)
  | where SyslogMessage contains "Failed password for invalid user"
  | where ProcessName =~ "sshd" 
  | parse kind=relaxed SyslogMessage with * "invalid user" user " from " ip " port" port " ssh2"
  | project user, ip, port, SyslogMessage, EventTime
  | summarize EventTimes = make_list(EventTime), PerHourCount = count() by ip, bin(EventTime, 4h), user
  | where PerHourCount > threshold
  | mvexpand EventTimes
  | extend EventTimes = tostring(EventTimes) 
  | summarize StartTimeUtc = min(EventTimes), EndTimeUtc = max(EventTimes), UserList = makeset(user), sum(PerHourCount) by IPAddress = ip
  | extend UserList = tostring(UserList) 
  | extend timestamp = StartTimeUtc, IPCustomEntity = IPAddress, AccountCustomEntity = UserList
entityMappings:
  - entityType: Account
    fieldMappings:
      - identifier: FullName
        columnName: AccountCustomEntity
  - entityType: IP
    fieldMappings:
      - identifier: Address
        columnName: IPCustomEntity

"""


class RuleTests(unittest.TestCase):
    def test_rule_validation(self):
        doc = yaml.full_load(test_rule)
        rule = ScheduledAlertRuleTemplate.from_yaml_template(doc)
        validator = ScheduledRuleValidator(rule)
        result = validator.validate()
        self.assertTrue(result)

class ValidatorTests(unittest.TestCase):
    def test_name_validation(self):
        doc = yaml.full_load(test_rule)
        rule = ScheduledAlertRuleTemplate.from_yaml_template(doc)
        validator = ScheduledRuleValidator(rule)
        result = validator._validate_name()
        self.assertTrue(result)  

    def test_display_name_validation(self):
        doc = yaml.full_load(test_rule)
        rule = ScheduledAlertRuleTemplate.from_yaml_template(doc)
        validator = ScheduledRuleValidator(rule)
        result = validator._validate_display_name()
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()