from pathlib import Path

import fitz

from app.services.ocr_service import run_ocr_on_page


SCANNED_TEXT_THRESHOLD = 40


def extract_pdf_pages(path: Path) -> dict:
    pages = []
    scanned_pages = []

    with fitz.open(path) as document:
        for index, page in enumerate(document, start=1):
            text = page.get_text("text").strip()
            ocr_used = False
            is_scanned = len(text) < SCANNED_TEXT_THRESHOLD

            if is_scanned:
                scanned_pages.append(index)
                try:
                    ocr_text = run_ocr_on_page(page)
                    if ocr_text:
                        text = ocr_text
                        ocr_used = True
                except Exception as exc:
                    text = text or f"OCR failed for page {index}: {exc}"

            pages.append(
                {
                    "page_number": index,
                    "text": text,
                    "has_text": len(text) >= SCANNED_TEXT_THRESHOLD,
                    "ocr_used": ocr_used,
                    "is_scanned": is_scanned,
                }
            )

    return {
        "pages": pages,
        "full_text": "\n\n".join(page["text"] for page in pages),
        "total_pages": len(pages),
        "scanned_pages": scanned_pages,
    }

