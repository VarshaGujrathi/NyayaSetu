import difflib

def compare_documents(old_text, new_text):
    old_lines = old_text.split('. ')
    new_lines = new_text.split('. ')

    diff = difflib.ndiff(old_lines, new_lines)

    changes = {
        "added": [],
        "removed": [],
        "modified": []
    }

    for line in diff:
        if line.startswith('+ '):
            changes["added"].append(line[2:])
        elif line.startswith('- '):
            changes["removed"].append(line[2:])
        elif line.startswith('? '):
            continue

    # modified = overlap heuristic
    for r in changes["removed"]:
        for a in changes["added"]:
            if len(set(r.split()) & set(a.split())) > 3:
                changes["modified"].append({"from": r, "to": a})

    return changes
