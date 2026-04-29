from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .utils import (
    extract_text_from_file,
    summarize_text,
    analyze_risks,
    extract_legal_entities_with_gemini,
    synthesize_speech,
    translate_text,
    AVAILABLE_TTS_LANGUAGES
)

from .compliance_engine import (
    evaluate_compliance,
    load_rules,
    detect_version
)

from .comparison_utils import compare_documents
from .clause_detector import detect_clauses
from .semantic_diff import compare_clauses_semantically
from .confidence_engine import calculate_confidence


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

    normalized=[]

    for item in risks:

        if not isinstance(item,dict):
            continue

        clause_text=(
            item.get("clause")
            or item.get("text")
            or item.get("sentence")
            or "Clause text unavailable"
        )

        item["clause"]=clause_text

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

def legal_simplifier(request):

    session_data=request.session.get(
        "legal_simplifier_data",
        {}
    )

    context={
        "languages":AVAILABLE_TTS_LANGUAGES,
        "selected_summary_language":
        session_data.get(
            "selected_summary_language",
            "en"
        ),
        "selected_clause_language":
        session_data.get(
            "selected_clause_language",
            "en"
        )
    }


    if request.method=="POST":

        # Upload Document
        if request.FILES.get("file"):

            uploaded_file=request.FILES["file"]

            text=extract_text_from_file(
                uploaded_file
            )

            summary=normalize_summary(
                summarize_text(text)
            )

            risky=normalize_risks(
                analyze_risks(text)
            )

            session_data={
                "filename":uploaded_file.name,
                "summary":summary,
                "summary_translated":None,
                "summary_audio":None,
                "selected_summary_language":"en",
                "selected_clause_language":"en",
                "risky":risky
            }

            request.session[
                "legal_simplifier_data"
            ]=session_data

            request.session.modified=True


        elif request.POST.get(
            "translate_action"
        ):

            action=request.POST.get(
                "translate_action"
            )

            language=request.POST.get(
                "language",
                "en"
            )

            session_data=request.session.get(
                "legal_simplifier_data",
                {}
            )

            if not session_data:
                return render(
                    request,
                    "legal_simplifier.html",
                    context
                )


            # SUMMARY TRANSLATION
            if action=="summary":

                session_data[
                    "selected_summary_language"
                ]=language

                base_summary=(
                    session_data.get("summary")
                    or "No summary available"
                )

                translated=(
                    translate_text(
                        base_summary,
                        language
                    )
                    or base_summary
                )

                session_data[
                    "summary_translated"
                ]=translated

                session_data[
                    "summary_audio"
                ]=synthesize_speech(
                    translated,
                    language
                )


            # CLAUSE TRANSLATION
            elif action=="clause":

                session_data[
                    "selected_clause_language"
                ]=language

                idx=int(
                    request.POST.get(
                        "clause_index",
                        -1
                    )
                )

                risky=session_data.get(
                    "risky",
                    []
                )

                if 0<=idx<len(risky):

                    item=risky[idx]

                    clause_text=item["clause"]

                    translated=(
                        translate_text(
                            clause_text,
                            language
                        )
                        or clause_text
                    )

                    item[
                        "translation"
                    ]=translated

                    item[
                        "audio"
                    ]=synthesize_speech(
                        translated,
                        language
                    )


            request.session[
                "legal_simplifier_data"
            ]=session_data

            request.session.modified=True


    context.update(
        request.session.get(
            "legal_simplifier_data",
            {}
        )
    )

    return render(
        request,
        "legal_simplifier.html",
        context
    )


# ==========================================
# CLAUSE RISK INDICATOR
# ==========================================

def clause_risk_indicator(request):

    context={
        "languages":AVAILABLE_TTS_LANGUAGES,
        "selected_language":"en"
    }

    session_data=request.session.get(
        "clause_risk_data",
        {}
    )

    if request.method=="POST":

        if request.FILES.get("file"):

            uploaded_file=request.FILES["file"]

            text=extract_text_from_file(
                uploaded_file
            )

            risk_data=normalize_risks(
                analyze_risks(text)
            )

            session_data={
                "filename":uploaded_file.name,
                "risk_data":risk_data
            }

            request.session[
                "clause_risk_data"
            ]=session_data

            request.session.modified=True


        elif request.POST.get(
            "translate_action"
        ):

            language=request.POST.get(
                "language",
                "en"
            )

            clause_index=int(
                request.POST.get(
                    "clause_index",
                    -1
                )
            )

            if (
                0<=clause_index<
                len(
                    session_data.get(
                        "risk_data",
                        []
                    )
                )
            ):

                item=session_data[
                    "risk_data"
                ][clause_index]

                translated=(
                    translate_text(
                        item["clause"],
                        language
                    )
                    or item["clause"]
                )

                item["translation"]=translated

                item["audio"]=synthesize_speech(
                    translated,
                    language
                )

                request.session[
                    "clause_risk_data"
                ]=session_data

                request.session.modified=True

    context.update(session_data)

    return render(
        request,
        "clause_risk_indicator.html",
        context
    )


# ==========================================
# COMPLIANCE
# ==========================================

@csrf_exempt
def compliance_alerts(request):

    if request.method=="POST":

        doc_type=request.POST.get(
            "document_type"
        )

        uploaded_file=request.FILES.get(
            "document"
        )

        if not uploaded_file:
            return render(
                request,
                "compliance_alerts.html",
                {"error":"No file uploaded"}
            )

        raw_text=extract_text_from_file(
            uploaded_file
        )

        evidence=extract_legal_entities_with_gemini(
            raw_text
        )

        rules=load_rules(doc_type)

        alerts=evaluate_compliance(
            evidence,
            rules
        )

        return render(
            request,
            "compliance_alerts.html",
            {
                "document_type":doc_type,
                "alerts":alerts,
                "extracted":evidence
            }
        )

    return render(
        request,
        "compliance_alerts.html"
    )


# ==========================================
# DOCUMENT COMPARISON
# ==========================================

def document_comparison(request):

    context={}

    if request.method=="POST":

        doc1=request.FILES.get("doc1")
        doc2=request.FILES.get("doc2")

        if not doc1 or not doc2:
            return render(
                request,
                "document_comparison.html",
                context
            )

        text1=extract_text_from_file(doc1)
        text2=extract_text_from_file(doc2)

        changes=compare_documents(
            text1,
            text2
        )

        version=detect_version(
            changes
        )

        old_clauses=detect_clauses(text1)
        new_clauses=detect_clauses(text2)

        semantic_results=compare_clauses_semantically(
            old_clauses,
            new_clauses
        )

        confidence=calculate_confidence(
            changes,
            semantic_results
        )

        context.update({
            "changes":changes,
            "version":version,
            "semantic_results":semantic_results,
            "confidence":confidence
        })

    return render(
        request,
        "document_comparison.html",
        context
    )