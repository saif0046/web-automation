"""
CAPTCHA Image Preprocessing
---------------------------
Cleans and enhances CAPTCHA images before sending to OCR.
These steps improve accuracy significantly.
"""

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import cv2

def preprocess_image_pil(img: Image.Image, method: str = "minimal") -> Image.Image:
    """
    Apply preprocessing levels to CAPTCHA image.

    Levels:
        minimal  - Slight sharpening & contrast (fastest).
        medium   - Noise removal + binary thresholding.
        aggressive - Heavy denoise, adaptive thresholding, morphological filters.

    Returns:
        PIL.Image: Processed image.
    """
    img = img.convert("L") # Convert to grayscale
    img_array = np.array(img)

    if method == "minimal":
        enhancer = ImageEnhance.Contrast(Image.fromarray(img_array))
        img = enhancer.enhance(1.5).filter(ImageFilter.SHARPEN)
        return img

    elif method == "medium":
        img_array = cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
        _, img_array = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    else:  # aggressive
        img_array = cv2.GaussianBlur(img_array, (5, 5), 0)
        img_array = cv2.adaptiveThreshold(
            img_array, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            21, 10
        )
        # Ensure high contrast
        if img_array.mean() < 127:
            img_array = cv2.bitwise_not(img_array)

        # Remove small artifacts
        img_array = cv2.morphologyEx(
            img_array,
            cv2.MORPH_OPEN,
            np.ones((2, 2), np.uint8)
        )

    return Image.fromarray(img_array)
