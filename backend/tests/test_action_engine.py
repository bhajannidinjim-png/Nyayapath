from app.extraction.action_engine import generate_actions


def test_generate_actions_detects_directive_with_deadline_and_department():
    pages = [
        {
            "page_number": 1,
            "text": "The Municipal Corporation is directed to remove the encroachment within 30 days and file a compliance report.",
        }
    ]

    actions = generate_actions(pages)

    assert len(actions) == 1
    assert actions[0]["department"] == "Municipal Department"
    assert actions[0]["deadline"] == "within 30 days"
    assert actions[0]["priority"] == "High"
    assert actions[0]["verification_status"] == "pending"


def test_generate_actions_ignores_non_directive_background_text():
    pages = [
        {
            "page_number": 1,
            "text": "The court considered the facts and reviewed earlier correspondence between the parties.",
        }
    ]

    assert generate_actions(pages) == []
