from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once (safe for dev, CPU OK)
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_change(old_text, new_text, threshold=0.75):
    """
    Returns similarity score and whether meaning changed
    """
    if not old_text or not new_text:
        return {
            "similarity": 0.0,
            "meaning_changed": True
        }

    emb_old = model.encode([old_text])
    emb_new = model.encode([new_text])

    similarity = cosine_similarity(emb_old, emb_new)[0][0]

    return {
        "similarity": round(float(similarity), 3),
        "meaning_changed": similarity < threshold
    }


def compare_clauses_semantically(old_clauses, new_clauses):
    """
    Clause-wise semantic comparison
    """
    results = []

    min_len = min(len(old_clauses), len(new_clauses))

    for i in range(min_len):
        old = old_clauses[i]
        new = new_clauses[i]

        semantic_result = semantic_change(old["text"], new["text"])

        results.append({
            "clause": old["clause_id"],
            "old": old["text"],
            "new": new["text"],
            "similarity": semantic_result["similarity"],
            "meaning_changed": semantic_result["meaning_changed"]
        })

    return results
