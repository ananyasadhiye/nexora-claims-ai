def generate_reason(route, data, validation):

    if validation["missing"]:
        return "Missing required fields detected"

    if validation["invalid"]:
        return "Invalid data format found"

    if route == "Fast-track":
        return "Low risk claim with clean data"

    if route == "Investigation Flag":
        return "Fraud indicators detected"

    return "Standard manual review required"