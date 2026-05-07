import re

try:
    import spacy

    NLP = spacy.blank("en")
    NLP.add_pipe("sentencizer")
except Exception:
    NLP = None


DIRECTIVE_SIGNALS = [
    "directed to",
    "is directed",
    "are directed",
    "shall",
    "must",
    "ordered",
    "hereby",
    "comply",
    "submit",
    "file",
    "furnish",
    "pay",
    "deposit",
    "list the matter",
    "take steps",
    "ensure",
]

DEPARTMENT_RULES = {
    "Municipal Department": ["municipal", "corporation", "civic", "building", "encroachment"],
    "Police Department": ["police", "fir", "investigation", "station house", "commissioner"],
    "Revenue Department": ["collector", "revenue", "tahsildar", "land records"],
    "Health Department": ["hospital", "medical", "health", "doctor"],
    "Education Department": ["school", "college", "university", "education"],
    "Public Works Department": ["road", "bridge", "pwd", "public works", "highway"],
    "Finance / Treasury": ["pay", "compensation", "arrears", "pension", "salary", "deposit"],
    "Court Registry": ["list the matter", "registry", "next hearing", "posted"],
    "Legal Department": ["appeal", "review petition", "special leave", "limitation"],
}

ACTION_RULES = [
    ("Payment / Compensation", ["pay", "deposit", "compensation", "arrears", "refund"]),
    ("Information Submission", ["submit", "file", "furnish", "produce", "affidavit", "report"]),
    ("Hearing / Listing", ["list the matter", "next hearing", "posted", "registry"]),
    ("Appeal Consideration", ["appeal", "review", "special leave", "limitation"]),
    ("Administrative Follow-up", ["take steps", "ensure", "implement", "appoint", "constitute"]),
    ("Compliance", ["comply", "shall", "directed", "ordered", "must"]),
]

DEADLINE_PATTERNS = [
    r"within\s+(?:a\s+)?(?:period\s+of\s+)?\d+\s+(?:days?|weeks?|months?)",
    r"on or before\s+[0-9]{1,2}[./-][0-9]{1,2}[./-][0-9]{2,4}",
    r"not later than\s+[A-Za-z0-9 ,./-]{4,30}",
    r"by\s+[0-9]{1,2}[./-][0-9]{1,2}[./-][0-9]{2,4}",
    r"forthwith|immediately",
]


def _paragraphs(pages):
    for page in pages:
        chunks = re.split(r"\n\s*\n|(?<=\.)\s+(?=[A-Z][a-z])", page.get("text", ""))
        for chunk in chunks:
            cleaned = re.sub(r"\s+", " ", chunk).strip()
            if len(cleaned) >= 45:
                yield page["page_number"], cleaned


def _signal_score(text):
    lower = text.lower()
    matches = [signal for signal in DIRECTIVE_SIGNALS if signal in lower]
    modal_bonus = 0.15 if re.search(r"\b(shall|must|directed|ordered)\b", lower) else 0
    return min(1.0, (len(matches) * 0.14) + modal_bonus), matches


def _deadline(text):
    for pattern in DEADLINE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return "Not specified"


def _action_type(text):
    lower = text.lower()
    for action_type, words in ACTION_RULES:
        if any(word in lower for word in words):
            return action_type
    return "Compliance"


def _department(text):
    lower = text.lower()
    for department, words in DEPARTMENT_RULES.items():
        if any(word in lower for word in words):
            return department
    return "Concerned Government Department"


def _priority(text, deadline):
    lower = text.lower()
    if any(word in lower for word in ["immediately", "forthwith", "contempt", "urgent"]):
        return "High"
    if deadline != "Not specified":
        return "High" if "days" in deadline.lower() else "Medium"
    if "may consider" in lower or "liberty" in lower:
        return "Low"
    return "Medium"


def _summary(text):
    sentence = next(iter(NLP(text).sents), text) if NLP else text
    summary = str(sentence).strip()
    return summary[:260] + ("..." if len(summary) > 260 else "")


def generate_actions(pages):
    actions = []
    seen = set()

    for page_number, paragraph in _paragraphs(pages):
        score, signals = _signal_score(paragraph)
        if score < 0.24:
            continue

        key = paragraph[:120].lower()
        if key in seen:
            continue
        seen.add(key)

        deadline = _deadline(paragraph)
        action_type = _action_type(paragraph)
        priority = _priority(paragraph, deadline)
        department = _department(paragraph)
        confidence = min(0.95, score + (0.12 if deadline != "Not specified" else 0) + (0.08 if department != "Concerned Government Department" else 0))

        actions.append(
            {
                "action_type": action_type,
                "action_summary": _summary(paragraph),
                "department": department,
                "deadline": deadline,
                "priority": priority,
                "compliance_requirement": "Human officer must verify the directive, assign ownership, and track completion before closure.",
                "appeal_consideration": "Review limitation period and grounds for appeal if the direction is adverse or operationally infeasible.",
                "confidence": round(confidence, 2),
                "source_text": paragraph,
                "extraction_reason": f"Directive paragraph detected using signals: {', '.join(signals[:5])}. Classified by action and department rules.",
                "page_reference": page_number,
                "verification_status": "pending",
            }
        )

    return actions

