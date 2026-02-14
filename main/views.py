from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import re
import os

from .utils import (
    extract_text_from_file,
    extract_text_from_path,
    summarize_text,
    find_risky_clauses,
    extract_legal_entities_with_gemini
)
from .compliance_engine import evaluate_compliance, load_rules

# ============================================================
# BASIC PAGES
# ============================================================

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def voice_text_interaction(request):
    return render(request, "voice_text_interaction.html")

def smart_form_autofill(request):
    return render(request, "smart_form_autofill.html")

# ============================================================
# LEGAL SIMPLIFIER
# ============================================================

def legal_simplifier(request):
    context = {}
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        text = extract_text_from_file(uploaded_file)
        summary = summarize_text(text)
        risky = find_risky_clauses(text)

        context = {
            "summary": summary,
            "risky": risky,
            "filename": uploaded_file.name
        }
    return render(request, "legal_simplifier.html", context)

# ============================================================
# CLAUSE RISK INDICATOR
# ============================================================

def analyze_clause_risks(text):
    risk_keywords = {
        "High": [
            "terminate without notice", "not liable", "sole discretion",
            "binding arbitration", "indemnify", "forfeit", "void"
        ],
        "Medium": [
            "limited liability", "subject to change",
            "automatic renewal", "non-compliance", "breach"
        ],
        "Low": [
            "privacy policy", "terms of use", "confidentiality"
        ]
    }

    clauses = re.split(r'(?<=[.?!])\s+', text)
    risk_data = []

    for clause in clauses:
        for level, keywords in risk_keywords.items():
            if any(keyword in clause.lower() for keyword in keywords):
                risk_data.append({
                    "text": clause.strip(),
                    "level": level
                })
                break

    return risk_data


def clause_risk_indicator(request):
    context = {}
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        text = extract_text_from_file(uploaded_file)
        risk_data = analyze_clause_risks(text)

        context = {
            "filename": uploaded_file.name,
            "risk_data": risk_data
        }

    return render(request, "clause_risk_indicator.html", context)

# ============================================================
# COMPLIANCE ALERTS (EVIDENCE-BASED)
# ============================================================

@csrf_exempt
def compliance_alerts(request):
    if request.method == "POST":
        doc_type = request.POST.get("document_type")
        uploaded_file = request.FILES.get("document")

        if not uploaded_file:
            return render(
                request,
                "compliance_alerts.html",
                {"error": "No file uploaded"}
            )

        fs = FileSystemStorage(location="media/")
        filename = fs.save(uploaded_file.name, uploaded_file)
        full_path = fs.path(filename)

        try:
            # Step 1: Extract raw text
            raw_text = extract_text_from_path(full_path)

            # Step 2: Gemini → evidence extraction
            evidence = extract_legal_entities_with_gemini(raw_text)

            # Step 3: Load document-specific rules
            rules = load_rules(doc_type)

            # Step 4: Evaluate compliance using evidence
            alerts = evaluate_compliance(evidence, rules)

            return render(
                request,
                "compliance_alerts.html",
                {
                    "document_type": doc_type,
                    "alerts": alerts,
                    "extracted": evidence
                }
            )
        finally:
            # Cleanup uploaded file
            if os.path.exists(full_path):
                os.remove(full_path)

    return render(request, "compliance_alerts.html")

# ============================================================
# DOCUMENT COMPARISON (FIXED)
# ============================================================

from django.shortcuts import render

from .utils import extract_text_from_file
from .comparison_utils import compare_documents
from .compliance_engine import detect_version
from .clause_detector import detect_clauses
from .semantic_diff import compare_clauses_semantically
from .confidence_engine import calculate_confidence


def document_comparison(request):
    context = {}

    if request.method == "POST":
        doc1 = request.FILES.get("doc1")
        doc2 = request.FILES.get("doc2")

        if not doc1 or not doc2:
            return render(request, "document_comparison.html", context)

        # 1️⃣ Extract text (RAM only)
        text1 = extract_text_from_file(doc1)
        text2 = extract_text_from_file(doc2)

        # 2️⃣ Basic diff
        changes = compare_documents(text1, text2)

        # 3️⃣ Version detection
        version = detect_version(changes)

        # 4️⃣ Clause detection
        old_clauses = detect_clauses(text1)
        new_clauses = detect_clauses(text2)

        # 5️⃣ Semantic comparison
        semantic_results = compare_clauses_semantically(
            old_clauses,
            new_clauses
        )

        # 6️⃣ Confidence score
        confidence = calculate_confidence(
            changes,
            semantic_results
        )

        # 7️⃣ Pass to template
        context.update({
            "changes": changes,
            "version": version,
            "semantic_results": semantic_results,
            "confidence": confidence,
        })

    return render(request, "document_comparison.html", context)


