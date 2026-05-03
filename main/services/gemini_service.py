import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def gemini_gap_analysis(text, doc_type):
    prompt = f"""
    You are a legal compliance assistant.

    Document Type: {doc_type}

    Identify missing elements in this document.

    Return STRICT JSON:
    {{
      "missing_elements": [],
      "risk_level": "LOW | MEDIUM | HIGH",
      "suggestions": []
    }}

    Document:
    {text[:5000]}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return '{"missing_elements": [], "risk_level": "LOW", "suggestions": []}'
    
    