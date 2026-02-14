def calculate_confidence(changes, semantic_results):
    score = 0

    score += len(changes["added"]) * 2
    score += len(changes["removed"]) * 2
    score += sum(1 for s in semantic_results if s["meaning_changed"]) * 3

    max_score = 20
    confidence = min(score / max_score, 1.0)

    return round(confidence, 2)
