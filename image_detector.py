from PIL import Image
import pytesseract


# Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image_path):
    """
    Extracts English and Hindi text from an image using Tesseract OCR.
    """

    try:
        image = Image.open(image_path)

        # English + Hindi OCR
        text = pytesseract.image_to_string(
            image,
            lang="eng+hin"
        )

        return text.strip()

    except Exception as e:
        print("OCR Error:", e)
        return ""