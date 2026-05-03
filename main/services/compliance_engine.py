import re
from main.rules.document_rules import DOCUMENT_RULES
from main.utils.pattern_matcher import pattern_check


def evaluate_compliance(text, doc_type):
    rules = DOCUMENT_RULES.get(doc_type, {})

    # Rule-based detection
    rule_missing = pattern_check(text, rules)

    # Risk logic
    if len(rule_missing) > 5:
        risk = "HIGH"
    elif len(rule_missing) > 2:
        risk = "MEDIUM"
    elif len(rule_missing) > 0:
        risk = "LOW"
    else:
        risk = "LOW"

    alerts = []

    for item in rule_missing:
        alerts.append({
            "severity": "Critical",
            "message": f"Missing: {item}"
        })

    return alerts, risk