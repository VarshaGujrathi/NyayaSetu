import re

CLAUSE_PATTERN = re.compile(
    r'(?P<number>(\d+(\.\d+)*|clause\s+\d+|section\s+[ivx]+))',
    re.IGNORECASE
)

def detect_clauses(text):
    clauses = []
    matches = list(CLAUSE_PATTERN.finditer(text))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        clause_text = text[start:end].strip()

        clauses.append({
            "clause_id": match.group("number"),
            "text": clause_text
        })

    return clauses
