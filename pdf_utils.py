"""
pdf_utils.py
------------
Handles PDF text extraction using PyMuPDF (fitz).
Step 2 Addition: OCR fallback using pytesseract for scanned pages.

Logic:
- Try to extract text normally using PyMuPDF
- If a page has less than 30 characters → it's likely scanned
- Convert that page to an image using fitz (no pdf2image needed)
- Run pytesseract OCR on that image to get text
- Replace the empty page text with OCR result
"""

import fitz  # PyMuPDF
import os
import pytesseract
from PIL import Image
import io



# ─────────────────────────────────────────────
# OCR FALLBACK FUNCTION (NEW IN STEP 2)
# ─────────────────────────────────────────────

def ocr_single_page(page) -> str:
    """
    Convert a single PyMuPDF page to an image and run OCR on it.

    Args:
        page: A fitz.Page object (one page from the PDF)

    Returns:
        Extracted text string from OCR, or empty string if OCR fails.
    """
    try:
        # Step 1: Render the page as a pixel map (image)
        # Matrix(2, 2) = 2x zoom for better OCR accuracy (higher DPI)
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)

        # Step 2: Convert pixmap to PNG bytes, then to PIL Image
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))

        # Step 3: Run pytesseract OCR on the PIL image
        # lang='eng' = English; you can add '+hin' for Hindi later
        ocr_text = pytesseract.image_to_string(img, lang='eng')

        # Step 4: Clean up and return
        return ocr_text.strip()

    except Exception as e:
        # If OCR fails for any reason, return empty string (don't crash)
        print(f"OCR failed on page: {str(e)}")
        return ""


# ─────────────────────────────────────────────
# MAIN EXTRACTION FUNCTION (UPDATED)
# ─────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extract text from each page of a PDF file.
    If a page has less than 30 characters, OCR is used as fallback.

    Args:
        pdf_path: Full path to the uploaded PDF file.

    Returns:
        A dict with:
            - 'pages'        : list of {page_num, text, has_text, ocr_used}
            - 'full_text'    : all pages joined as one string
            - 'total_pages'  : int
            - 'scanned_pages': list of page numbers that needed OCR
    """

    # Check file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    result = {
        "pages": [],
        "full_text": "",
        "total_pages": 0,
        "scanned_pages": []
    }

    try:
        # Open the PDF with PyMuPDF
        doc = fitz.open(pdf_path)
        result["total_pages"] = len(doc)

        all_text_parts = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            # Step 1: Try normal text extraction first
            text = page.get_text("text").strip()

            ocr_used = False  # Track whether OCR was needed

            # Step 2: If text is too short, page is likely scanned → use OCR
            if len(text) < 30:
                print(f"Page {page_num + 1}: Low text ({len(text)} chars) → Running OCR...")

                # Run OCR on this page
                ocr_text = ocr_single_page(page)

                if ocr_text:
                    text = ocr_text       # Replace empty text with OCR result
                    ocr_used = True
                    result["scanned_pages"].append(page_num + 1)
                else:
                    # OCR also returned nothing — mark as scanned but empty
                    result["scanned_pages"].append(page_num + 1)

            has_text = len(text) > 20  # Final check after OCR attempt

            # Step 3: Store page result
            result["pages"].append({
                "page_num": page_num + 1,
                "text": text,
                "has_text": has_text,
                "ocr_used": ocr_used
            })

            if has_text:
                label = f"--- Page {page_num + 1} {'[OCR]' if ocr_used else ''} ---"
                all_text_parts.append(f"{label}\n{text}")

        doc.close()

        # Join all pages into one full text string
        result["full_text"] = "\n\n".join(all_text_parts)

    except Exception as e:
        raise RuntimeError(f"Failed to extract PDF text: {str(e)}")

    return result


# ─────────────────────────────────────────────
# METADATA FUNCTION (UNCHANGED FROM STEP 1)
# ─────────────────────────────────────────────

def get_pdf_metadata(pdf_path: str) -> dict:
    """
    Extract basic metadata from the PDF (title, author, page count).
    """
    try:
        doc = fitz.open(pdf_path)
        meta = doc.metadata
        meta["page_count"] = len(doc)
        doc.close()
        return meta
    except Exception as e:
        return {"error": str(e), "page_count": 0}


# ─────────────────────────────────────────────
# FILE SAVE FUNCTION (UNCHANGED FROM STEP 1)
# ─────────────────────────────────────────────

def save_uploaded_file(uploaded_file, save_dir: str = "uploads") -> str:
    """
    Save a Streamlit uploaded file object to disk.
    """
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path