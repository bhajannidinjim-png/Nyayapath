from app.extraction.metadata_extractor import extract_metadata


def test_extract_metadata_finds_core_fields():
    pages = [
        {
            "page_number": 1,
            "text": """
            IN THE HIGH COURT OF KARNATAKA AT BENGALURU
            WRIT PETITION NO. 1234 OF 2024
            DATED: 12 March 2024
            Asha Kumar ... Petitioner
            State of Karnataka ... Respondent
            """,
        }
    ]

    metadata = extract_metadata(pages)

    assert metadata["court_name"]["value"].startswith("IN THE HIGH COURT")
    assert "1234" in metadata["case_number"]["value"]
    assert metadata["judgment_date"]["value"] == "12 March 2024"
    assert metadata["petitioner"]["confidence"] > 0
    assert metadata["respondent"]["confidence"] > 0
