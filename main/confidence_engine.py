def calculate_confidence(changes, semantic_results=None):
    """
    Calculates a dynamic, realistic confidence score for the AI's analysis.
    Rather than blindly adding to 1.0, it evaluates document alignment quality.
    """
    if not semantic_results:
        semantic_results = []
        
    total_changes = len(changes["added"]) + len(changes["removed"]) + len(changes["modified"])
    
    # If documents are perfectly identical
    if total_changes == 0:
        return 1.00
        
    # Base confidence in the AI diffing algorithm
    confidence = 0.98
    
    # Penalty 1: Highly noisy documents (too many fragmented changes) reduce alignment confidence
    noise_penalty = min(total_changes * 0.005, 0.15)
    
    # Penalty 2: Drastic semantic meaning shifts lower the confidence of a "1:1" comparison
    meaning_shifts = sum(1 for s in semantic_results if s.get("meaning_changed", False))
    semantic_penalty = min(meaning_shifts * 0.015, 0.20)
    
    # Calculate final score (bounded between 0.65 and 0.98 for realism)
    final_score = confidence - noise_penalty - semantic_penalty
    
    return round(max(0.65, final_score), 2)