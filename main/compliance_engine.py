import json
import os

# --------------------------------------------------
# LOAD COMPLIANCE RULES
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_DIR = os.path.join(BASE_DIR, "compliance_rules")


def load_rules(doc_type):
    """
    Load rules JSON for selected document type
    """
    path = os.path.join(RULES_DIR, f"{doc_type}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------
# SAFE EVIDENCE ACCESS (CRITICAL FIX)
# --------------------------------------------------

def get_evidence_value(evidence, evidence_key):
    """
    Safely resolve nested keys like:
    'licensor.names'
    'execution.date'
    'stamp_registration.stamp_present'
    """
    if not evidence_key:
        return None

    parts = evidence_key.split(".")
    current = evidence

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None  # 🔑 Missing evidence is allowed

    return current


# --------------------------------------------------
# EVIDENCE-BASED COMPLIANCE EVALUATION
# --------------------------------------------------

def evaluate_compliance(evidence, rules):
    """
    Compare extracted evidence vs compliance rules
    """
    alerts = []

    for rule in rules:
        field = rule["Field_Name"]
        requirement = rule["Requirement"]
        evidence_key = rule.get("Evidence_Key")
        min_count = rule.get("Min_Count", 1)
        allow_partial = rule.get("Allow_Partial", False)

        value = get_evidence_value(evidence, evidence_key)

        # ---- Count evidence ----
        count = 0
        if isinstance(value, list):
            count = len(value)
        elif isinstance(value, bool):
            count = 1 if value else 0
        elif isinstance(value, str):
            count = 1 if value.strip() else 0

        # ---- Decision logic ----
        if count == 0:
            severity = "Critical"
            if allow_partial:
                severity = "Review"

            alerts.append({
                "field": field,
                "severity": severity,
                "message": f"No clear evidence found for {field}"
            })

        elif count < min_count:
            alerts.append({
                "field": field,
                "severity": "Review",
                "message": f"Partial evidence found for {field}"
            })

        # else → Compliant → no alert

    return alerts


def detect_version(changes):
    score = len(changes["added"]) - len(changes["removed"])

    if score > 0:
        return "Document B is newer"
    elif score < 0:
        return "Document A is newer"
    return "Version unclear"
