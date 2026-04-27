def normalize_input(data: dict) -> dict:
    """Normalize string inputs and ensure consistent types."""
    normalized = {}
    for key, value in data.items():
        if isinstance(value, str):
            v = value.strip().lower()
            if v in {"yes", "no", "skip"}:
                normalized[key] = v
            else:
                normalized[key] = "invalid"
        else:
            normalized[key] = value
    return normalized


def validate_input(data: dict) -> list[str]:
    required = [
        "priority_done", "blocker_external", "anxious", "energized", "flat",
        "goal_action", "focus_minutes", "repeated_mistake", "rule_exists",
    ]
    return [f for f in required if f not in data]


def coerce_focus_minutes(value):
    """Convert focus to nonnegative int if possible."""
    if isinstance(value, int):
        return max(0, value)
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return "invalid"


def evaluate_priority_status(d):
    if d["priority_done"] in ("skip", "invalid") or d["blocker_external"] in ("skip", "invalid"):
        return "incomplete"
    if d["priority_done"] == "yes":
        return "done"
    if d["blocker_external"] == "yes":
        return "external_miss"
    return "self_miss"


def evaluate_emotion(d):
    if any(d[k] in ("skip", "invalid") for k in ["anxious", "energized", "flat"]):
        return "incomplete"
    # explicit conflict resolution
    if d["anxious"] == "yes" or d["flat"] == "yes":
        return "negative"
    if d["energized"] == "yes":
        return "positive"
    return "neutral"


def evaluate_progress(d):
    f = coerce_focus_minutes(d["focus_minutes"])
    if d["goal_action"] in ("skip", "invalid") or f == "invalid":
        return "incomplete"
    if d["goal_action"] != "yes":
        return "none"
    return "deep" if f >= 30 else "light"


def evaluate_improvement(d):
    if d["repeated_mistake"] in ("skip", "invalid"):
        return "incomplete"
    if d["repeated_mistake"] != "yes":
        return "none"
    if d["rule_exists"] in ("skip", "invalid"):
        return "incomplete"
    return "recommit_rule" if d["rule_exists"] == "yes" else "define_new_rule"


def run_reflection_agent(data: dict) -> dict:
    missing = validate_input(data)
    if missing:
        return {"error": "missing_fields", "missing": missing}

    d = normalize_input(data)
    return {
        "priority_status": evaluate_priority_status(d),
        "emotion": evaluate_emotion(d),
        "progress": evaluate_progress(d),
        "improvement": evaluate_improvement(d),
    }


# --- Example usage ---
if __name__ == "__main__":
    test_input = {
        "priority_done": "Yes",
        "blocker_external": "no",
        "anxious": "no",
        "energized": "Yes",
        "flat": "no",
        "goal_action": "yes",
        "focus_minutes": "45",
        "repeated_mistake": "yes",
        "rule_exists": "no",
    }

    print(run_reflection_agent(test_input))
