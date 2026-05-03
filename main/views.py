import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from .utils import (
    extract_text_from_file,
    extract_text_from_path,
    summarize_text,
    analyze_risks,
    extract_legal_entities_with_gemini,
    # synthesize_speech,
    # translate_text,
    AVAILABLE_TTS_LANGUAGES
)

from services.language_service import (
    translate_text_pipeline,
    text_to_speech_pipeline
)

from .compliance_engine import (
    evaluate_compliance,
    load_rules,
    detect_version,
    get_evidence_value
)

from .comparison_utils import compare_documents
from .clause_detector import detect_clauses
from .semantic_diff import compare_clauses_semantically
from .confidence_engine import calculate_confidence
from django.core.files.storage import FileSystemStorage

# ==========================================
# NORMALIZERS
# ==========================================

def normalize_summary(summary):
    if not summary:
        return "No summary generated."

    # catches accidental literal template text
    if str(summary).strip() in ["{{ summary }}", "{ summary }"]:
        return "Summary generation failed."

    return str(summary).strip()


def normalize_risks(risks):

    normalized = []

    for item in risks:

        if not isinstance(item, dict):
            continue

        clause_text = (
            item.get("clause")
            or item.get("text")
            or item.get("sentence")
            or "Clause text unavailable"
        )

        item["clause"] = clause_text

        item.setdefault(
            "risk_level",
            "Medium"
        )

        item.setdefault(
            "risk_category",
            "General"
        )

        item.setdefault(
            "explanation",
            "Potential legal risk detected."
        )

        item.setdefault(
            "translation",
            None
        )

        item.setdefault(
            "audio",
            None
        )

        normalized.append(item)

    return normalized


# ==========================================
# BASIC PAGES
# ==========================================

def index(request):
    return render(
        request,
        "index.html"
    )


def home(request):
    return render(
        request,
        "home.html"
    )


def voice_text_interaction(request):
    return render(
        request,
        "voice_text_interaction.html"
    )


def smart_form_autofill(request):
    return render(
        request,
        "smart_form_autofill.html"
    )


# ==========================================
# LEGAL SIMPLIFIER
# ==========================================

# def legal_simplifier(request):

#     from services.language_service import (
#         translate_text_pipeline,
#         text_to_speech_pipeline
#     )

#     session_data = request.session.get(
#         "legal_simplifier_data",
#         {}
#     )

#     context = {
#         "languages": AVAILABLE_TTS_LANGUAGES,
#         "selected_summary_language": session_data.get(
#             "selected_summary_language", "en"
#         ),
#         "selected_clause_language": session_data.get(
#             "selected_clause_language", "en"
#         )
#     }

#     if request.method == "POST":

#         # ==========================================
#         # FILE UPLOAD + INITIAL PROCESSING
#         # ==========================================
#         if request.FILES.get("file"):

#             uploaded_file = request.FILES["file"]

#             text = extract_text_from_file(uploaded_file)

#             summary = normalize_summary(
#                 summarize_text(text)
#             )

#             risky = normalize_risks(
#                 analyze_risks(text)
#             )

#             session_data = {
#                 "filename": uploaded_file.name,
#                 "summary": summary,
#                 "summary_translated": None,
#                 "summary_audio": None,
#                 "selected_summary_language": "en",
#                 "selected_clause_language": "en",
#                 "risky": risky
#             }

#             request.session["legal_simplifier_data"] = session_data
#             request.session.modified = True

#         # ==========================================
#         # TRANSLATION + AUDIO
#         # ==========================================
#         elif request.POST.get("translate_action"):

#             action = request.POST.get("translate_action")
#             language = request.POST.get("language", "en")

#             session_data = request.session.get(
#                 "legal_simplifier_data", {}
#             )

#             if not session_data:
#                 return render(
#                     request,
#                     "legal_simplifier.html",
#                     context
#                 )

#             # ======================================
#             # SUMMARY TRANSLATION + AUDIO
#             # ======================================
#             if action == "summary":

#                 session_data["selected_summary_language"] = language

#                 base_summary = (
#                     session_data.get("summary")
#                     or "No summary available"
#                 )

#                 # ✅ Translation using M2M100
#                 translated = translate_text_pipeline(
#                     base_summary,
#                     language
#                 )

#                 session_data["summary_translated"] = translated

#                 # ✅ TTS using gTTS
#                 session_data["summary_audio"] = text_to_speech_pipeline(
#                     translated,
#                     language
#                 )

#             # ======================================
#             # CLAUSE TRANSLATION + AUDIO
#             # ======================================
#             elif action == "clause":

#                 session_data["selected_clause_language"] = language

#                 idx = int(
#                     request.POST.get("clause_index", -1)
#                 )

#                 risky = session_data.get("risky", [])

#                 if 0 <= idx < len(risky):

#                     item = risky[idx]

#                     clause_text = item["clause"]

#                     # ✅ Translation
#                     translated = translate_text_pipeline(
#                         clause_text,
#                         language
#                     )

#                     item["translation"] = translated

#                     # ✅ TTS
#                     item["audio"] = text_to_speech_pipeline(
#                         translated,
#                         language
#                     )

#             request.session["legal_simplifier_data"] = session_data
#             request.session.modified = True

#     # ==========================================
#     # FINAL CONTEXT RENDER
#     # ==========================================
#     context.update(
#         request.session.get(
#             "legal_simplifier_data", {}
#         )
#     )

#     return render(
#         request,
#         "legal_simplifier.html",
#         context
#     )


def legal_simplifier(request):
    from services.language_service import translate_text_pipeline, text_to_speech_pipeline

    session_data = request.session.get("legal_simplifier_data", {})
    context = {
        "languages": AVAILABLE_TTS_LANGUAGES,
        "selected_summary_language": session_data.get("selected_summary_language", "en"),
    }

    if request.method == "POST":
        # FILE UPLOAD: Only generate summary
        if request.FILES.get("file"):
            uploaded_file = request.FILES["file"]
            text = extract_text_from_file(uploaded_file)
            summary = normalize_summary(summarize_text(text))

            session_data = {
                "filename": uploaded_file.name,
                "summary": summary,
                "summary_translated": None,
                "summary_audio": None,
                "selected_summary_language": "en",
            }
            request.session["legal_simplifier_data"] = session_data
            request.session.modified = True

        # TRANSLATION: Only for summary
        elif request.POST.get("translate_action") == "summary":
            language = request.POST.get("language", "en")
            session_data = request.session.get("legal_simplifier_data", {})

            if session_data:
                session_data["selected_summary_language"] = language
                base_summary = session_data.get("summary") or "No summary available"
                
                translated = translate_text_pipeline(base_summary, language)
                session_data["summary_translated"] = translated
                session_data["summary_audio"] = text_to_speech_pipeline(translated, language)

                request.session["legal_simplifier_data"] = session_data
                request.session.modified = True

    context.update(request.session.get("legal_simplifier_data", {}))
    return render(request, "legal_simplifier.html", context)


# ==========================================
# CLAUSE RISK INDICATOR
# ==========================================

# def clause_risk_indicator(request):

#     from services.language_service import (
#         translate_text_pipeline,
#         text_to_speech_pipeline
#     )

#     context = {
#         "languages": AVAILABLE_TTS_LANGUAGES,
#         "selected_language": "en"
#     }

#     session_data = request.session.get(
#         "clause_risk_data",
#         {}
#     )

#     if request.method == "POST":

#         # ==========================================
#         # FILE UPLOAD
#         # ==========================================
#         if request.FILES.get("file"):

#             uploaded_file = request.FILES["file"]

#             text = extract_text_from_file(
#                 uploaded_file
#             )

#             risk_data = normalize_risks(
#                 analyze_risks(text)
#             )

#             session_data = {
#                 "filename": uploaded_file.name,
#                 "risk_data": risk_data
#             }

#             request.session["clause_risk_data"] = session_data
#             request.session.modified = True

#         # ==========================================
#         # TRANSLATION + AUDIO
#         # ==========================================
#         elif request.POST.get("translate_action"):

#             language = request.POST.get("language", "en")

#             clause_index = int(
#                 request.POST.get("clause_index", -1)
#             )

#             if (
#                 0 <= clause_index <
#                 len(session_data.get("risk_data", []))
#             ):

#                 item = session_data["risk_data"][clause_index]

#                 clause_text = item.get("clause", "")

#                 # ✅ Translation (M2M100)
#                 translated = translate_text_pipeline(
#                     clause_text,
#                     language
#                 )

#                 item["translation"] = translated

#                 # ✅ TTS (gTTS)
#                 item["audio"] = text_to_speech_pipeline(
#                     translated,
#                     language
#                 )

#                 request.session["clause_risk_data"] = session_data
#                 request.session.modified = True

#     context.update(session_data)

#     return render(
#         request,
#         "clause_risk_indicator.html",
#         context
#     )


def clause_risk_indicator(request):
    from services.language_service import translate_text_pipeline, text_to_speech_pipeline

    session_data = request.session.get("clause_risk_data", {})
    context = {
        "languages": AVAILABLE_TTS_LANGUAGES,
        "selected_language": session_data.get("selected_language", "en")
    }

    if request.method == "POST":
        # FILE UPLOAD: Only analyze risks
        if request.FILES.get("file"):
            uploaded_file = request.FILES["file"]
            text = extract_text_from_file(uploaded_file)
            risk_data = normalize_risks(analyze_risks(text))

            session_data = {
                "filename": uploaded_file.name,
                "risk_data": risk_data,
                "selected_language": "en"
            }
            request.session["clause_risk_data"] = session_data
            request.session.modified = True

        # TRANSLATION: Only for specific clauses
        elif request.POST.get("translate_action") == "clause":
            language = request.POST.get("language", "en")
            idx = int(request.POST.get("clause_index", -1))
            session_data = request.session.get("clause_risk_data", {})

            if session_data and 0 <= idx < len(session_data.get("risk_data", [])):
                item = session_data["risk_data"][idx]
                translated = translate_text_pipeline(item["clause"], language)
                item["translation"] = translated
                item["audio"] = text_to_speech_pipeline(translated, language)
                
                session_data["selected_language"] = language
                request.session["clause_risk_data"] = session_data
                request.session.modified = True

    context.update(request.session.get("clause_risk_data", {}))
    return render(request, "clause_risk_indicator.html", context)

    
# ============================================================
# COMPLIANCE ALERTS
# ============================================================
import re

def extract_document_summary(text):
    text = text.replace("\n", " ")

    data = {
        "execution": {
            "date": None,
            "place": None,
            "method": "Registered Agreement"
        },
        "licensor": {"names": []},
        "licensees": {"names": []},
        "witnesses": {"names": []},
        "period": {"from": None, "to": None},
        "financial": {"license_fee": None, "deposit": None}
    }

    # Execution
    match = re.search(
        r"executed on (\d{2}/\d{2}/\d{4}) at ([A-Za-z ]+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["execution"]["date"] = match.group(1)
        data["execution"]["place"] = match.group(2).strip()

    # Licensor
    licensor_match = re.findall(
        r"Name:\s*Mr\.?\s*([A-Za-z ]+).*?Licensor",
        text,
        re.IGNORECASE
    )
    if licensor_match:
        data["licensor"]["names"] = [licensor_match[0].strip()]

    # Licensees
    licensees = re.findall(r"Name:\s*Mr\.?\s*([A-Za-z ]+)", text)
    if licensees:
        data["licensees"]["names"] = [name.strip() for name in licensees[1:]]

    # Period
    period_match = re.search(
        r"commencing from (\d{2}/\d{2}/\d{4}) and ending on (\d{2}/\d{2}/\d{4})",
        text,
        re.IGNORECASE
    )
    if period_match:
        data["period"]["from"] = period_match.group(1)
        data["period"]["to"] = period_match.group(2)

    # License Fee
    fee_match = re.search(
        r"Rs\.?\s?(\d{4,6}).*?per month",
        text,
        re.IGNORECASE
    )
    if fee_match:
        data["financial"]["license_fee"] = f"Rs. {fee_match.group(1)} / month"

    # Deposit
    deposit_match = re.search(
        r"Rs\.?\s?(\d{4,7}).*?deposit",
        text,
        re.IGNORECASE
    )
    if deposit_match:
        data["financial"]["deposit"] = f"Rs. {deposit_match.group(1)}"

    # Witness
    witness_block = re.search(
        r"(witness of execution.*?)(admission of execution|$)",
        text,
        re.IGNORECASE
    )

    if witness_block:
        block = witness_block.group(1)

        names = re.findall(
            r"(?:Mr\.|Ms\.|Mrs\.)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})",
            block
        )

        blacklist_words = [
            "Document", "No", 
            "Not Required", 
            "Flat", "Floor", "Road",
            "Building", "Sector", "Block",
            "Highway", "East", "West"
        ]

        cleaned = []

        for name in names:
            name = name.strip()

            if any(word.lower() in name.lower() for word in blacklist_words):
                continue

            if re.search(r"\d", name):
                continue

            cleaned.append(name)

        data["witnesses"]["names"] = list(set(cleaned))

    # ✅ CRITICAL FIX
    return data

def compliance_alerts(request):
    context = {}

    if request.method == "POST":
        document_type = request.POST.get("document_type")
        uploaded_file = request.FILES.get("document")

        if uploaded_file:
            fs = FileSystemStorage(location="media/")
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            try:
                # Extract text
                text = extract_text_from_path(file_path)

                # Extract summary
                extracted = extract_document_summary(text)

                # Load rules and evaluate compliance
                rules = load_rules(document_type)
                alerts = evaluate_compliance(extracted, rules)

                # Calculate risk level based on alerts
                critical_count = sum(1 for a in alerts if a.get("severity") == "Critical")
                review_count = sum(1 for a in alerts if a.get("severity") == "Review")
                
                if critical_count > 0:
                    risk = "HIGH"
                elif review_count > 0:
                    risk = "MEDIUM"
                else:
                    risk = "LOW"

                context = {
                    "document_type": document_type,
                    "extracted": extracted,
                    "alerts": alerts,
                    "risk": risk,
                }

            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)

    return render(request, "compliance_alerts.html", context)

# ==========================================
# DOCUMENT COMPARISON
# ==========================================

def document_comparison(request):

    context = {}

    if request.method == "POST":

        doc1 = request.FILES.get("doc1")
        doc2 = request.FILES.get("doc2")

        if not doc1 or not doc2:
            return render(
                request,
                "document_comparison.html",
                context
            )

        text1 = extract_text_from_file(doc1)
        text2 = extract_text_from_file(doc2)

        changes = compare_documents(
            text1,
            text2
        )

        version = detect_version(
            changes
        )

        old_clauses = detect_clauses(text1)
        new_clauses = detect_clauses(text2)

        semantic_results = compare_clauses_semantically(
            old_clauses,
            new_clauses
        )

        confidence = calculate_confidence(
            changes,
            semantic_results
        )

        context.update({
            "changes": changes,
            "version": version,
            "semantic_results": semantic_results,
            "confidence": confidence
        })

    return render(
        request,
        "document_comparison.html",
        context
    )

#Smart Form Autofill

def smart_form_autofill(request):
    return render(request, 'smart_form_autofill.html')