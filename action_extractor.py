"""
action_extractor.py
-------------------
Rule-based extraction engine for NyayPath.
Extracts structured action items from court judgment text.
No paid APIs. No LLMs. Pure Python regex + keyword logic.
"""

import re
from datetime import datetime


# ─────────────────────────────────────────────
# KEYWORD LISTS
# ─────────────────────────────────────────────

# Words that signal a directive or order
DIRECTIVE_KEYWORDS = [
    "shall", "must", "directed", "ordered", "hereby orders",
    "is required to", "ought to", "mandated", "instructed",
    "directed to", "required to", "ought to comply",
    "is directed", "are directed", "comply with", "ensure that",
    "take action", "take steps", "file", "submit", "furnish",
    "produce", "deposit", "pay", "vacate", "demolish", "restore",
    "provide", "implement", "establish", "constitute", "appoint"
]

# Words that signal a deadline
DEADLINE_KEYWORDS = [
    "within", "before", "by", "not later than", "no later than",
    "forthwith", "immediately", "within a period of",
    "on or before", "within weeks", "within days", "within months"
]

# Department inference keywords
DEPARTMENT_MAP = {
    "Municipal Corporation": ["municipal", "corporation", "bbmp", "mcgm", "nmc", "civic body"],
    "State Government": ["state government", "state of", "chief secretary", "state"],
    "Central Government": ["union of india", "central government", "ministry", "union government"],
    "Police Department": ["police", "sp ", "dsp", "inspector general", "law enforcement"],
    "Revenue Department": ["collector", "district collector", "revenue", "tahsildar"],
    "Forest Department": ["forest", "wildlife", "tree", "environment"],
    "Public Works Department": ["pwd", "public works", "road", "highway", "construction"],
    "Health Department": ["health", "hospital", "medical", "doctor", "sanitation"],
    "Education Department": ["school", "college", "university", "education", "teacher"],
    "Water Board": ["water", "sewage", "drainage", "bwssb", "jal board"],
    "Electricity Board": ["electricity", "power", "bescom", "discom", "energy"],
    "Transport Department": ["transport", "rto", "vehicle", "traffic"],
}

# Priority keywords
HIGH_PRIORITY_KEYWORDS = ["immediately", "forthwith", "urgent", "stay", "contempt", "penalty", "fine"]
LOW_PRIORITY_KEYWORDS = ["may", "consider", "if possible", "endeavour", "try to"]


# ─────────────────────────────────────────────
# HELPER: Extract dates from text
# ─────────────────────────────────────────────

def extract_dates(text: str) -> list:
    """
    Find all date patterns in a piece of text.
    Returns list of date strings found.
    """
    patterns = [
        r'\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b',          # 12/03/2024
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b',  # 12 March 2024
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',  # March 12, 2024
        r'\bwithin\s+\d+\s+(?:days?|weeks?|months?)\b',           # within 30 days
        r'\bwithin\s+(?:a\s+)?(?:period\s+of\s+)?\d+\s+(?:days?|weeks?|months?)\b',
    ]
    dates_found = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates_found.extend(matches)
    return list(set(dates_found))  # Remove duplicates


# ─────────────────────────────────────────────
# HELPER: Infer responsible department
# ─────────────────────────────────────────────

def infer_department(text: str) -> str:
    """
    Scan sentence for department keywords and return best match.
    Returns 'Not Specified' if nothing matches.
    """
    text_lower = text.lower()
    for dept, keywords in DEPARTMENT_MAP.items():
        for kw in keywords:
            if kw in text_lower:
                return dept
    return "Not Specified"


# ─────────────────────────────────────────────
# HELPER: Determine priority
# ─────────────────────────────────────────────

def determine_priority(text: str, has_deadline: bool) -> str:
    """
    Assign priority based on keywords and deadline presence.
    High / Medium / Low
    """
    text_lower = text.lower()

    # Check high priority signals
    for kw in HIGH_PRIORITY_KEYWORDS:
        if kw in text_lower:
            return "High"

    # Explicit deadline = high priority
    if has_deadline:
        return "High"

    # Check low priority signals
    for kw in LOW_PRIORITY_KEYWORDS:
        if kw in text_lower:
            return "Low"

    # Default
    return "Medium"


# ─────────────────────────────────────────────
# HELPER: Determine confidence
# ─────────────────────────────────────────────

def determine_confidence(sentence: str, has_deadline: bool, has_department: bool) -> str:
    """
    Assign confidence level to an extracted action.
    High   = explicit deadline + department found
    Medium = keyword match only
    Low    = weak inference
    """
    if has_deadline and has_department:
        return "High"
    elif has_deadline or has_department:
        return "Medium"
    else:
        return "Low"


# ─────────────────────────────────────────────
# CASE METADATA EXTRACTION
# ─────────────────────────────────────────────

def extract_case_metadata(text: str) -> dict:
    """
    Extract high-level case info from the judgment text.
    Returns dict with court_name, case_title, judgment_date, parties.
    """
    metadata = {
        "court_name": "Not identified",
        "case_title": "Not identified",
        "judgment_date": "Not identified",
        "petitioner": "Not identified",
        "respondent": "Not identified",
    }

    lines = text.split("\n")

    # --- Court Name ---
    court_patterns = [
        r'(High Court of [A-Za-z\s]+)',
        r'(Supreme Court of India)',
        r'(District Court[A-Za-z\s,]*)',
        r'(IN THE .+? COURT)',
        r'(BEFORE THE .+? COURT)',
    ]
    for line in lines[:30]:  # Courts usually mentioned in first 30 lines
        for pattern in court_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                metadata["court_name"] = match.group(1).strip()
                break

    # --- Case Title (W.P., Crl., Civil Appeal etc.) ---
    case_patterns = [
        r'(W\.?P\.?\s*\(?\w*\)?\s*No\.?\s*\d+[\w\s\/]*\d{4})',
        r'(Civil Appeal No\.?\s*\d+[\w\s\/]*\d{4})',
        r'(Criminal Appeal No\.?\s*\d+[\w\s\/]*\d{4})',
        r'(Writ Petition.{0,50}\d{4})',
        r'(Petition No\.?\s*\d+[\w\s\/]*\d{4})',
        r'(Case No\.?\s*\d+[\w\s\/]*\d{4})',
    ]
    for line in lines[:40]:
        for pattern in case_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                metadata["case_title"] = match.group(1).strip()
                break

    # --- Judgment Date ---
    date_pattern = r'\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b'
    date_matches = re.findall(date_pattern, text[:2000], re.IGNORECASE)
    if date_matches:
        metadata["judgment_date"] = date_matches[0]

    # --- Parties (Petitioner vs Respondent) ---
    versus_pattern = r'([A-Z][A-Za-z\s\.\,]+)\s+[Vv](?:ersus|s\.?)\s+([A-Z][A-Za-z\s\.\,]+)'
    versus_match = re.search(versus_pattern, text[:3000])
    if versus_match:
        metadata["petitioner"] = versus_match.group(1).strip()[:80]
        metadata["respondent"] = versus_match.group(2).strip()[:80]

    return metadata


# ─────────────────────────────────────────────
# MAIN ACTION EXTRACTION FUNCTION
# ─────────────────────────────────────────────

def extract_actions(full_text: str) -> list:
    """
    Extract structured action items from full judgment text.

    Steps:
    1. Split text into sentences
    2. Check each sentence for directive keywords
    3. If match → extract deadline, department, priority, confidence
    4. Return list of structured action dicts

    Args:
        full_text: Complete extracted text from PDF

    Returns:
        List of action dicts:
        [{ action, deadline, department, priority, confidence, source_text }]
    """

    actions = []

    # Clean text: remove page markers added by pdf_utils
    clean_text = re.sub(r'--- Page \d+ (?:\[OCR\])? ---', '', full_text)

    # Split into sentences (split on . or \n)
    sentences = re.split(r'(?<=[.!?])\s+|\n+', clean_text)

    seen_actions = set()  # Avoid duplicate actions

    for sentence in sentences:
        sentence = sentence.strip()

        # Skip very short sentences (less than 15 chars = not useful)
        if len(sentence) < 15:
            continue

        # Check if sentence contains any directive keyword
        sentence_lower = sentence.lower()
        is_directive = any(kw in sentence_lower for kw in DIRECTIVE_KEYWORDS)

        if not is_directive:
            continue

        # --- Extract deadline ---
        dates = extract_dates(sentence)
        deadline = dates[0] if dates else "Not specified"
        has_deadline = len(dates) > 0

        # --- Infer department ---
        department = infer_department(sentence)
        has_department = department != "Not Specified"

        # --- Determine priority ---
        priority = determine_priority(sentence, has_deadline)

        # --- Determine confidence ---
        confidence = determine_confidence(sentence, has_deadline, has_department)

        # --- Clean action text (truncate if too long) ---
        action_text = sentence[:300] + "..." if len(sentence) > 300 else sentence

        # Deduplicate (skip if very similar action already added)
        action_key = action_text[:60].lower()
        if action_key in seen_actions:
            continue
        seen_actions.add(action_key)

        actions.append({
            "action": action_text,
            "deadline": deadline,
            "department": department,
            "priority": priority,
            "confidence": confidence,
            "source_text": sentence[:200]
        })

    return actions


# ─────────────────────────────────────────────
# FULL PIPELINE ENTRY POINT
# ─────────────────────────────────────────────

def run_extraction(full_text: str) -> dict:
    """
    Master function: runs full extraction pipeline.
    Call this from app.py.

    Returns:
        {
            "metadata": { court_name, case_title, ... },
            "actions": [ { action, deadline, department, ... }, ... ],
            "total_actions": int,
            "high_priority_count": int,
        }
    """
    metadata = extract_case_metadata(full_text)
    actions = extract_actions(full_text)

    high_count = sum(1 for a in actions if a["priority"] == "High")
    medium_count = sum(1 for a in actions if a["priority"] == "Medium")
    low_count = sum(1 for a in actions if a["priority"] == "Low")

    return {
        "metadata": metadata,
        "actions": actions,
        "total_actions": len(actions),
        "high_priority_count": high_count,
        "medium_priority_count": medium_count,
        "low_priority_count": low_count,
    }
