from abc import ABC, abstractmethod

class AlertStrategy(ABC):
    @abstractmethod
    def trigger_alert(self, component: str, error: str): pass

class PagerDutyStrategy(AlertStrategy):
    def trigger_alert(self, component: str, error: str):
        print(f"🚨 [PAGERDUTY P0] Calling SRE On-Call for {component}! Error: {error}")

class SlackStrategy(AlertStrategy):
    def trigger_alert(self, component: str, error: str):
        print(f"💬 [SLACK P2] Notifying team channel. {component} issue: {error}")

def get_alert_strategy(severity: str) -> AlertStrategy:
    if severity == "P0": return PagerDutyStrategy()
    return SlackStrategy()