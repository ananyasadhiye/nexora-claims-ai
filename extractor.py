import json
import requests
import re
import streamlit as st

# ================= API =================

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"


# ================= TEXT CLEAN =================

def preprocess_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ================= DOCUMENT CLASSIFICATION =================

def classify_document(text):

    text = text.lower()

    instruction_keywords = [
        "problem statement", "assignment",
        "assessment", "instructions", "submission"
    ]

    claim_keywords = [
        "policy number", "incident",
        "damage", "insured", "accident"
    ]

    resume_keywords = [
        "education", "projects",
        "skills", "linkedin", "github"
    ]

    if sum(k in text for k in instruction_keywords) >= 2:
        return "other"

    if sum(k in text for k in resume_keywords) > 2:
        return "irrelevant"

    if sum(k in text for k in claim_keywords) == 0:
        return "irrelevant"

    return "claim"


# ================= EMPTY FORM CHECK =================

def is_empty_form(text):

    patterns = [
        r"policy number\s*:\s*\w+",
        r"incident date\s*:\s*\d",
        r"location\s*:\s*\w+",
        r"claimant\s*:\s*\w+",
        r"estimated damage\s*:\s*\d+"
    ]

    matches = sum(1 for p in patterns if re.search(p, text.lower()))

    return matches < 2


# ================= JSON CLEANER =================

def clean_json(text):

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return "{}"


# ================= FIELD EXTRACTION =================

def extract_fields(text):

    text = preprocess_text(text)

    doc_type = classify_document(text)

    # 🚫 Invalid document checks
    if doc_type == "irrelevant":
        return {"_meta": "irrelevant_document"}

    if doc_type == "other":
        return {"_meta": "non_claim_document"}

    if is_empty_form(text):
        return {"_meta": "empty_form"}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Extract insurance claim fields from the text.

Return ONLY valid JSON.

Fields:
policy_number
policyholder_name
effective_dates
incident_date
incident_time
location
description
claimant
third_parties
contact_details
asset_type
asset_id
estimated_damage
claim_type
attachments
initial_estimate

Text:
{text}
"""

    payload = {

        "model": "openai/gpt-4o-mini",

        "messages": [
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],

        "temperature": 0
    }

    try:

        response = requests.post(URL, headers=headers, json=payload)

        response.raise_for_status()

        data = response.json()

        content = data["choices"][0]["message"]["content"]

        cleaned = clean_json(content)

        parsed = json.loads(cleaned)

        return parsed

    except json.JSONDecodeError:

        st.warning("⚠️ AI returned invalid JSON. Using fallback extraction.")

        return {}

    except Exception as e:

        st.error(f"Extractor Error: {e}")

        return {}