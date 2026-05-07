import io

import fitz
import pytesseract
from PIL import Image


def run_ocr_on_page(page: fitz.Page) -> str:
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    image = Image.open(io.BytesIO(pixmap.tobytes("png")))
    return pytesseract.image_to_string(image, lang="eng").strip()

