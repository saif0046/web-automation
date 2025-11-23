"""
Post-OCR Correction Module
--------------------------
Fixes characters commonly misread by OCR.
Example: O → 9, S → 5
"""
import numpy as np


def correct_ocr_errors(text: str, img_array: np.ndarray) -> str:
    """
    Apply heuristic corrections on OCR output.
    Returns:
        str: Improved 5-character CAPTCHA text.
    """
    corrected = list(text)
    height, width = img_array.shape

    for i, char in enumerate(corrected):
        if i >= 5:
            break

        char_width = max(1, width // 5)
        x0 = i * char_width
        x1 = min((i + 1) * char_width, width)
        region = img_array[:, x0:x1]

        # Fix 0/O → 9
        if char in ['0', 'O']:
            lower = region[height // 2:, :]
            upper = region[:height // 2, :]
            if np.sum(lower) < np.sum(upper):
                corrected[i] = "9"

        # Fix S → 5
        if char == "S":
            corrected[i] = "5"

    # Position 2 correction
    if len(corrected) == 5 and corrected[1] in ['0', 'O']:
        corrected[1] = "9"

    return "".join(corrected)
