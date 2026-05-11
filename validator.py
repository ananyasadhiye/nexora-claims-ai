import re
from datetime import datetime


# =========================
# Utility validators
# =========================
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False


def is_valid_phone(phone):
    if not phone:
        return False
    return re.fullmatch(r"\d{10}", phone.strip()) is not None


def safe_float(value):
    try:
        return float(value)
    except:
        return None


# =========================
# Main validation function
# =========================
def validate_fields(data):
    required = [
        "policy_number",
        "incident_date",
        "location",
        "claimant",
        "estimated_damage",
        "claim_type"
    ]

    missing = []
    invalid = []
    inconsistent = []
    warnings = []

    score = 100

    # =========================
    # 1. Missing fields
    # =========================
    for field in required:
        if not data.get(field):
            missing.append(field)
            score -= 10

    # =========================
    # 2. Date validation
    # =========================
    if data.get("incident_date") and not is_valid_date(data["incident_date"]):
        invalid.append("incident_date")
        score -= 8

    # =========================
    # 3. Contact validation (safe)
    # =========================
    contact = data.get("contact_details")
    if contact:
        try:
            phone = contact.split(",")[0].strip()
            if not is_valid_phone(phone):
                invalid.append("contact_details")
                score -= 5
        except:
            invalid.append("contact_details")
            score -= 5

    # =========================
    # 4. Damage validation
    # =========================
    damage = safe_float(data.get("estimated_damage"))
    if damage is None:
        if data.get("estimated_damage"):
            invalid.append("estimated_damage")
            score -= 8
    else:
        if damage < 0:
            inconsistent.append("negative_damage")
            score -= 15

    # =========================
    # 5. Policy vs Incident date logic
    # =========================
    try:
        if data.get("effective_dates") and data.get("incident_date"):
            start, end = data["effective_dates"].split("to")

            start = datetime.strptime(start.strip(), "%Y-%m-%d")
            end = datetime.strptime(end.strip(), "%Y-%m-%d")
            incident = datetime.strptime(data["incident_date"], "%Y-%m-%d")

            if incident < start:
                inconsistent.append("incident_before_policy")
                score -= 20

            if incident > end:
                inconsistent.append("incident_after_policy")
                score -= 20
    except:
        if data.get("effective_dates"):
            invalid.append("effective_dates")
            score -= 8

    # =========================
    # 6. Estimate mismatch
    # =========================
    est1 = safe_float(data.get("initial_estimate"))
    est2 = safe_float(data.get("estimated_damage"))

    if est1 is not None and est2 is not None:
        diff_ratio = abs(est1 - est2) / max(est1, est2)

        if diff_ratio > 0.5:
            inconsistent.append("high_estimate_mismatch")
            score -= 15
        elif diff_ratio > 0.3:
            warnings.append("moderate_estimate_difference")
            score -= 5

    # =========================
    # 7. Semantic validation
    # =========================
    desc = (data.get("description") or "").lower()

    if damage:
        if damage < 5000 and any(w in desc for w in ["total loss", "severe", "major"]):
            inconsistent.append("damage_description_conflict")
            score -= 15

        if damage > 100000 and any(w in desc for w in ["minor", "scratch"]):
            inconsistent.append("damage_description_conflict")
            score -= 15

    # =========================
    # 8. Claim type mismatch
    # =========================
    claim_type = (data.get("claim_type") or "").lower()

    if claim_type == "injury" and "injury" not in desc:
        inconsistent.append("injury_mismatch")
        score -= 10

    if claim_type == "vehicle" and not any(w in desc for w in ["car", "vehicle", "bike"]):
        warnings.append("weak_vehicle_context")

    # =========================
    # 9. Fraud signals
    # =========================
    fraud_keywords = ["fraud", "staged", "fake", "intentional"]

    if any(word in desc for word in fraud_keywords):
        inconsistent.append("fraud_signal_detected")
        score -= 25

    # =========================
    # 10. Logical gap checks
    # =========================
    if damage and damage > 0 and not data.get("claimant"):
        inconsistent.append("missing_claimant_with_damage")
        score -= 10

    # =========================
    # 11. Final score grading
    # =========================
    score = max(0, min(score, 100))

    if score >= 80:
        quality = "high"
    elif score >= 50:
        quality = "medium"
    else:
        quality = "low"

    return {
        "missing": missing,
        "invalid": invalid,
        "inconsistent": inconsistent,
        "warnings": warnings,
        "confidence_score": score,
        "quality": quality
    }