# ==========================================================
# utils.py
# ==========================================================

import os
import re
import json
import pickle
import base64
from io import BytesIO

# ---------------- File Parsing ----------------
import fitz
import pdfplumber
import docx
from PIL import Image
import pytesseract

# ---------------- ML / NLP ----------------
import spacy
import torch
import requests

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# ---------------- TTS ----------------
from gtts import gTTS

# ---------------- Gemini ----------------
from google import genai
from django.conf import settings


# ==========================================================
# INITIALIZATION
# ==========================================================

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

nlp = spacy.load("en_core_web_sm")

client = genai.Client(
    api_key=settings.GOOGLE_API_KEY
)

# ==========================================================
# KEYWORDS
# ==========================================================

PENALTY_TERMS = [
    "liable",
    "penalty",
    "breach",
    "termination",
    "fine",
    "indemnify",
    "compensation",
    "non-compliance",
    "forfeit",
    "void"
]

# ==========================================================
# Text-to-Speech
# ==========================================================

AVAILABLE_TTS_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Malayalam": "ml"
}


def synthesize_speech(text, lang="en"):
    if not text or not text.strip():
        return None

    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        mp3_buffer = BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)

        encoded_audio = base64.b64encode(mp3_buffer.read()).decode("utf-8")
        return f"data:audio/mp3;base64,{encoded_audio}"

    except Exception as e:
        print("TTS error:", e)
        return None


def translate_text(text, target_language):
    if not text or not text.strip():
        return None

    if not target_language:
        target_language = "en"

    # Support passing either a language name or a code.
    if len(target_language) > 2:
        reverse_map = {code: name for name, code in AVAILABLE_TTS_LANGUAGES.items()}
        target_language = next(
            (code for name, code in AVAILABLE_TTS_LANGUAGES.items() if name.lower() == target_language.lower()),
            target_language
        )

    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "key": settings.GOOGLE_API_KEY
    }
    payload = {
        "q": text,
        "target": target_language,
        "format": "text"
    }

    try:
        response = requests.post(url, params=params, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data["data"]["translations"][0]["translatedText"]

    except Exception as e:
        print("Translation error:", e)
        return None


# ==========================================================
# MODEL PATHS
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

stage1_path = os.path.join(
    BASE_DIR,
    "models",
    "nyaysetu_stage1"
)

stage2_path = os.path.join(
    BASE_DIR,
    "models",
    "nyaysetu_stage2"
)

stage3_path = os.path.join(
    BASE_DIR,
    "models",
    "risk_type_svm.pkl"
)


# ==========================================================
# LOAD MODELS
# ==========================================================

CUSTOM_MODEL_READY=False

try:

    tokenizer1=AutoTokenizer.from_pretrained(
        stage1_path,
        local_files_only=True
    )

    risk_model=AutoModelForSequenceClassification.from_pretrained(
        stage1_path,
        local_files_only=True
    )

    tokenizer2=AutoTokenizer.from_pretrained(
        stage2_path,
        local_files_only=True
    )

    severity_model=AutoModelForSequenceClassification.from_pretrained(
        stage2_path,
        local_files_only=True
    )

    with open(stage3_path,"rb") as f:
        category_model=pickle.load(f)

    risk_model.eval()
    severity_model.eval()

    CUSTOM_MODEL_READY=True
    print("Custom risk models loaded successfully.")

except Exception as e:
    print("Model loading failed:",e)


# ==========================================================
# LABELS
# ==========================================================

severity_map={
    0:"Low",
    1:"Medium",
    2:"High"
}

category_explanations={

    "Penalty":
    "Penalty or monetary consequence detected.",

    "Financial":
    "Financial obligation risk detected.",

    "Liability":
    "Potential liability transfer detected.",

    "Restriction":
    "Restrictive contractual clause detected.",

    "Termination":
    "Termination-related risk detected."
}


# ==========================================================
# TEXT EXTRACTION
# ==========================================================

def normalize_text(text):

    text=text.lower()
    text=re.sub(r"\s+"," ",text)

    return text.strip()


def extract_text_from_pdf(uploaded_file):

    text=""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            page_text=page.extract_text()

            if page_text:
                text+=page_text+"\n"

    if not text.strip():

        uploaded_file.seek(0)

        with fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        ) as doc:

            for page in doc:

                pix=page.get_pixmap()

                img=Image.frombytes(
                    "RGB",
                    [pix.width,pix.height],
                    pix.samples
                )

                text += pytesseract.image_to_string(img)

    return normalize_text(text)


def extract_text_from_file(uploaded_file):

    file_name=uploaded_file.name.lower()

    if file_name.endswith(
        (".png",".jpg",".jpeg")
    ):

        image=Image.open(
            BytesIO(uploaded_file.read())
        )

        text=pytesseract.image_to_string(
            image
        )


    elif file_name.endswith(".pdf"):

        text=extract_text_from_pdf(
            uploaded_file
        )


    elif file_name.endswith(".docx"):

        doc=docx.Document(uploaded_file)

        text="\n".join(
            p.text for p in doc.paragraphs
        )

    else:

        uploaded_file.seek(0)

        text=uploaded_file.read().decode(
            "utf-8"
        )

    return normalize_text(text)


# PATH BASED EXTRACTION (needed by views)
def extract_text_from_path(path):

    with open(path,"rb") as f:
        return extract_text_from_file(f)


# ==========================================================
# GEMINI ENTITY EXTRACTION
# ==========================================================

def extract_legal_entities_with_gemini(
    document_text
):

    prompt=f"""
Return STRICT JSON only:

{{
"execution_date":[],
"execution_place":[],
"licensor_names":[],
"licensee_names":[],
"stamp_registration":[],
"witnesses":[],
"signatures":[]
}}

DOCUMENT:
{document_text[:12000]}
"""

    try:

        response=client.models.generate_content(
            model="models/gemini-1.0-pro",
            contents=prompt
        )

        return json.loads(
            response.text.strip()
        )

    except Exception as e:
        print("Gemini error:",e)
        return {}


# ==========================================================
# SUMMARIZATION
# ==========================================================

def summarize_text(text):

    if not text:
        return "No text found."


    if len(text)<1000:

        return summarizer(
            text,
            max_length=100,
            min_length=30,
            do_sample=False
        )[0]["summary_text"]


    chunks=[
        text[i:i+1000]
        for i in range(0,len(text),1000)
    ]

    summary=""

    for chunk in chunks[:3]:

        summary+= " " + summarizer(
            chunk,
            max_length=100,
            min_length=30,
            do_sample=False
        )[0]["summary_text"]

    return summary.strip()


# ==========================================================
# LEGACY RULE ENGINE
# ==========================================================

def find_risky_clauses(text):

    doc=nlp(text[:10000])

    return [

        sent.text

        for sent in doc.sents

        if any(
            t in sent.text.lower()
            for t in PENALTY_TERMS
        )
    ]


# ==========================================================
# MODEL PIPELINE
# ==========================================================

def split_clauses(text):

    clauses=re.split(
        r'(?<=[.;])\s+|\n+',
        text
    )

    return [
        c.strip()
        for c in clauses
        if len(c.strip())>20
    ]


def detect_risk(sentences):

    inputs=tokenizer1(
        sentences,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs=risk_model(**inputs)

    return torch.argmax(
        outputs.logits,
        dim=1
    ).tolist()


def detect_severity(sentences):

    inputs=tokenizer2(
        sentences,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs=severity_model(**inputs)

    return torch.argmax(
        outputs.logits,
        dim=1
    ).tolist()


def detect_category(sentences):
    return category_model.predict(sentences)


def explain_risk(category,severity):

    base=category_explanations.get(
        category,
        "Potential legal risk detected."
    )

    return f"{severity} Risk. {base}"


def analyze_risks(text):

    if not CUSTOM_MODEL_READY:

        return [
            {
                "clause":c,
                "risk_level":"Unknown",
                "risk_category":"Keyword Match",
                "explanation":"Fallback rule engine."
            }

            for c in find_risky_clauses(text)
        ]


    clauses=split_clauses(
        text[:15000]
    )

    if not clauses:
        return []

    preds=detect_risk(clauses)

    risky_clauses=[
        c for c,p in zip(
            clauses,preds
        ) if p==1
    ]

    if not risky_clauses:
        return []

    severity_preds=detect_severity(
        risky_clauses
    )

    categories=detect_category(
        risky_clauses
    )

    results=[]

    for clause,s,cat in zip(
        risky_clauses,
        severity_preds,
        categories
    ):

        if cat=="General":
            continue

        sev=severity_map[s]

        results.append({
            "clause":clause,
            "risk_level":sev,
            "risk_category":cat,
            "explanation":explain_risk(cat,sev)
        })

    return results