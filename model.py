def predict_priority(text):
    text = text.lower()

    if "urgent" in text or "immediately" in text or "danger" in text:
        return "High"
    elif "soon" in text or "issue" in text:
        return "Medium"
    else:
        return "Low"