def route_claim(data, validation):

    # Rule 1: Missing or invalid fields
    if validation.get("missing") or validation.get("invalid"):
        return "Manual Review"

    # Safe values
    desc = str(data.get("description", "")).lower()
    claim_type = str(data.get("claim_type", "")).lower()

    # Rule 2: Fraud keywords
    fraud_keywords = ["fraud", "staged", "inconsistent"]

    for word in fraud_keywords:
        if word in desc:
            return "Investigation Flag"

    # Rule 3: Injury claims
    if claim_type == "injury":
        return "Specialist Queue"

    # Rule 4: Fast-track for small damage
    try:
        damage = float(data.get("estimated_damage", 0))
        if damage < 25000:
            return "Fast-track"
    except:
        pass

    # Default
    return "Manual Review"