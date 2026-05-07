import re


COURT_PATTERN = re.compile(
    r"(IN THE\s+(?:HIGH|SUPREME|DISTRICT|COURT)[^\n]{0,90}|BEFORE THE\s+[^\n]{10,120})",
    re.IGNORECASE,
)
CASE_PATTERN = re.compile(
    r"((?:W\.?P\.?|C\.?A\.?|S\.?L\.?P\.?|CRL\.?A\.?|CIVIL APPEAL|WRIT PETITION|O\.?A\.?)\s*(?:NO\.?|NUMBER)?\s*[:\-]?\s*[\w./\- ]+\d{4})",
    re.IGNORECASE,
)
DATE_PATTERN = re.compile(
    r"(?:DATED|DATE OF JUDGMENT|PRONOUNCED ON|ORDER DATED)\s*[:\-]?\s*([0-9]{1,2}[./-][0-9]{1,2}[./-][0-9]{2,4}|[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
    re.IGNORECASE,
)


def _field(value="", confidence=0.0, source_text="", reason="", page_reference=None):
    return {
        "value": value or "Not found",
        "confidence": round(confidence, 2),
        "source_text": source_text,
        "extraction_reason": reason,
        "page_reference": page_reference,
    }


def _first_match(pattern, pages):
    for page in pages:
        match = pattern.search(page.get("text", ""))
        if match:
            return match.group(1).strip(), match.group(0).strip(), page["page_number"]
    return None, "", None


def _party_line(label, pages):
    label_group = f"(?:{label})"
    patterns = [
        re.compile(rf"([A-Z][A-Za-z .,&'-]{{2,120}})\s+\.{{0,3}}\s*{label_group}", re.IGNORECASE),
        re.compile(rf"{label_group}\s*[:\-]\s*([A-Z][A-Za-z .,&'-]{{2,120}})", re.IGNORECASE),
    ]
    for page in pages[:3]:
        for pattern in patterns:
            match = pattern.search(page.get("text", ""))
            if match and match.group(1):
                return match.group(1).strip(), match.group(0).strip(), page["page_number"]
    return None, "", None


def extract_metadata(pages):
    court, court_source, court_page = _first_match(COURT_PATTERN, pages[:2])
    case_no, case_source, case_page = _first_match(CASE_PATTERN, pages[:3])
    date, date_source, date_page = _first_match(DATE_PATTERN, pages[:4])
    petitioner, petitioner_source, petitioner_page = _party_line("petitioner|appellant", pages)
    respondent, respondent_source, respondent_page = _party_line("respondent", pages)

    return {
        "court_name": _field(court, 0.84 if court else 0, court_source, "Matched court heading pattern.", court_page),
        "case_number": _field(case_no, 0.82 if case_no else 0, case_source, "Matched common Indian case number formats.", case_page),
        "petitioner": _field(petitioner, 0.7 if petitioner else 0, petitioner_source, "Matched party label near petitioner/appellant.", petitioner_page),
        "respondent": _field(respondent, 0.7 if respondent else 0, respondent_source, "Matched party label near respondent.", respondent_page),
        "judgment_date": _field(date, 0.78 if date else 0, date_source, "Matched date label used in judgments.", date_page),
    }
