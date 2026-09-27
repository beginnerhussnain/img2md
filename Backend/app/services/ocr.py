import pytesseract
from PIL import Image
from lxml import etree
from pathlib import Path

# Hardcoded path — required on Windows so pytesseract can find the binary
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def run_ocr_hocr(image_path: Path, lang: str = "eng") -> etree._Element:
    """
    Run Tesseract in hOCR mode and return the parsed XML tree.
    hOCR gives us: page > carea > par > line > word (with bbox + confidence).
    """
    img = Image.open(image_path)

    # Upscale small images for better OCR accuracy
    if img.width < 1000:
        scale = 1000 / img.width
        img = img.resize((int(img.width * scale), int(img.height * scale)))

    hocr_bytes = pytesseract.image_to_pdf_or_hocr(
        img, extension="hocr", lang=lang, config="--psm 3"
    )
    return etree.fromstring(hocr_bytes)