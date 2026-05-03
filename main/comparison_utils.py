import difflib
import re

def get_word_level_diff(old_sent, new_sent):
    """Compares two sentences word-by-word to pinpoint exact changes."""
    # Split by spaces but preserve the whitespace for accurate reconstruction
    old_words = re.split(r'(\s+)', old_sent)
    new_words = re.split(r'(\s+)', new_sent)

    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    inline_html = ""
    details = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old_chunk = "".join(old_words[i1:i2])
        new_chunk = "".join(new_words[j1:j2])

        if tag == 'equal':
            inline_html += old_chunk
        elif tag == 'replace':
            inline_html += f'<del class="remove">{old_chunk}</del><ins class="add">{new_chunk}</ins>'
            if old_chunk.strip() or new_chunk.strip():
                details.append(f"Changed '{old_chunk.strip()}' to '{new_chunk.strip()}'")
        elif tag == 'delete':
            inline_html += f'<del class="remove">{old_chunk}</del>'
            if old_chunk.strip():
                details.append(f"Removed '{old_chunk.strip()}'")
        elif tag == 'insert':
            inline_html += f'<ins class="add">{new_chunk}</ins>'
            if new_chunk.strip():
                details.append(f"Added '{new_chunk.strip()}'")

    return inline_html, details


def compare_documents(old_text, new_text):
    old_clean = old_text.replace('\n', ' ')
    new_clean = new_text.replace('\n', ' ')
    
    old_sentences = [s.strip() for s in re.split(r'\.\s+', old_clean) if s.strip()]
    new_sentences = [s.strip() for s in re.split(r'\.\s+', new_clean) if s.strip()]

    changes = {
        "added": [],
        "removed": [],
        "modified": []
    }

    matcher = difflib.SequenceMatcher(None, old_sentences, new_sentences)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            old_chunk = ". ".join(old_sentences[i1:i2]) + "."
            new_chunk = ". ".join(new_sentences[j1:j2]) + "."
            
            # Run the nested word-level comparison
            inline_html, details = get_word_level_diff(old_chunk, new_chunk)
            
            changes["modified"].append({
                "from": old_chunk, 
                "to": new_chunk,
                "inline_html": inline_html,
                "details": details
            })

        elif tag == 'delete':
            chunk = ". ".join(old_sentences[i1:i2]) + "."
            changes["removed"].append(chunk)

        elif tag == 'insert':
            chunk = ". ".join(new_sentences[j1:j2]) + "."
            changes["added"].append(chunk)

    return changes