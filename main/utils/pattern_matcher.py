import re

# -------------------------
# PATTERNS
# -------------------------
PATTERNS = {
    "assignor": r"(assignor|transferor|seller)",
    "assignee": r"(assignee|transferee|buyer)",

    "consideration": r"(consideration|payment|amount|price|sum)",
    "amount": r"(amount|sum|total|rs\.?|inr)",

    "date": r"(date|executed on|agreement date)",
    "signatures": r"(signature|signed|signatory)",
    "witness": r"(witness|witnesses|in presence of|witness of execution)",

    "license fee": r"(license fee|rent|monthly fee|usage fee)",
    "duration": r"(duration|period|term|tenure)",
    "property description": r"(property|premises|flat|apartment|unit)",

    "termination": r"(termination|terminate|expiry)",
    "deposit": r"(deposit|security deposit|advance)",

    "stamp duty": r"(stamp duty|stamp charges)",
    "registration": r"(registration|registered|sub registrar)",
}

# -------------------------
# ✅ REQUIRED FUNCTION (FIX)
# -------------------------
def pattern_check(text, rules):
    text = text.lower()
    missing = []

    for item in rules.get("required", []):
        pattern = PATTERNS.get(item, item)

        if not re.search(pattern, text):
            missing.append(item)

    return missing


# -------------------------
# ✅ OPTIONAL WITNESS EXTRACTOR (SAFE)
# -------------------------
def extract_witnesses(text):
    witnesses = []

    match = re.search(
        r'witness of execution.*?(?=admission of execution|$)',
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        block = match.group()

        names = re.findall(
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b',
            block
        )

        witnesses.extend(names)

    return list(set(witnesses))