"""
OCR Engine Wrapper
------------------
Handles:
    - Creating EasyOCR reader
    - Running multi-stage preprocessing
    - Running OCR
    - Applying post-correction
"""
import warnings
import numpy as np
from PIL import Image
import easyocr
from .preprocess import preprocess_image_pil
from .error_correction import correct_ocr_errors

warnings.filterwarnings("ignore", message=".*pin_memory.*")


def get_reader(gpu=False):
    """
    Create EasyOCR reader instance.
    """
    return easyocr.Reader(['en'], gpu=gpu)


def read_captcha_from_file(path: str, reader):
    """
    Run OCR with 3 preprocessing levels.
    """
    img = Image.open(path)
    methods = ["minimal", "medium", "aggressive"]

    for method in methods:
        try:
            processed = preprocess_image_pil(img.copy(), method)
            print("Processed: ", processed)
            w, h = processed.size
            print("w, h: ", w, h)
            scaled = processed.resize((w * 3, h * 3))
            print("Scaled: ", scaled)
            arr = np.array(scaled)
            print("Arr: ", arr)

            results = reader.readtext(
                arr,
                detail=0,
                allowlist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            )
            print("RESULT- ", results)

            if not results:
                continue

            raw = results[0].replace(" ", "")

            final = correct_ocr_errors(raw, arr if arr.ndim == 2 else arr[:, :, 0])
            print("FINAL- ", final)

            if len(final) == 5:
                return final

        except Exception:
            continue

    return None
