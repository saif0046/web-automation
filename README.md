# CAPTCHA Solver using Pyppeteer & EasyOCR  
### A Fully Automated CAPTCHA Recognition & Submission System


It uses **Pyppeteer (browser automation)** A port (copy) of Puppeteer from JavaScript → Python and **EasyOCR (text extraction)** to capture, preprocess, read, and submit CAPTCHA text automatically.

---

# Features

- Automatically launches a browser
- Navigates to the CAPTCHA page
- Captures CAPTCHA screenshot
- Preprocesses image for higher accuracy
- Extracts text using EasyOCR
- Fixes common OCR mistakes (0,O→9, S→5, etc.)
- Types the CAPTCHA into input
- Submits the form automatically
- Logging and error handling

---

# Installation

### 1. Create & activate virtual environment

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate  # Linux / Mac
$ .venv\Scripts\activate     # Windows
```

### 2. Install dependencies inside the virtual environment

```bash
$ pip install -r requirements.txt
```

### 3. Run the main program

```bash
$ python3 -m src.main
```

### Image Preprocessing — How & Why I Used These Techniques
CAPTCHA images are intentionally distorted and contain noise that makes direct OCR inaccurate.  
When testing with raw CAPTCHA images, EasyOCR Tesseract OCR, and Tesseract.js was unable to reliably detect the 5-character text because:

- Characters had low contrast against the background  
- Noise pixels around the letters confused OCR  
- Some characters (0/O, S/5) looked almost identical  
- Uneven brightness caused broken edges  
- CAPTCHA had small distortions that needed correction

To solve this, I implemented **multi-stage image preprocessing** in `preprocess.py` and integrated it with OCR 
logic in `reader.py`.

OCR engines like EasyOCR, Tesseract OCR, and Tesseract.js struggle with noise-heavy images. I tried all three libraries,
but none of them produced accurate results.
If we want accurate results without using preprocessing, then we would need to train a custom OCR model using a large 
CAPTCHA training dataset that matches the same style and distortion.
Only after training such a model can we achieve high accuracy without applying preprocessing steps.

### Preprocessing Steps Explained
1. Grayscale Conversion (Refer to ocr/preprocess.py)
```bash
$ img.convert("L")
```
- Why: OCR works best on single-channel images. Removing color simplifies the data and makes thresholding more effective.

2. Contrast Enhancement (Refer to ocr/preprocess.py)
```bash
$ enhancer.enhance(1.5)
```
- Why: Increases the visibility of characters and strengthens edges, helping OCR correctly identify shapes.

3. Sharpening Filter (Refer to ocr/preprocess.py)
```bash
$ ImageFilter.SHARPEN
```
- Why: Makes text edges clearer and reduces blur. Very useful when CAPTCHA letters are slightly soft or distorted.

4. Noise Reduction (Denoising) (Refer to ocr/preprocess.py)
```bash
$ cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
```
- Why: Removes random noise pixels that often interfere with stroke detection. Without denoising, OCR sometimes read 
noise as actual characters.

5. Otsu Binary Thresholding (Refer to ocr/preprocess.py)
```bash
$ cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```
- Why: Automatically converts the image to pure black & white depending on optimal thresholding.This emphasizes 
characters and removes mid-tones that confuse OCR.

6. Adaptive Thresholding (Refer to ocr/preprocess.py)
```bash
$ cv2.adaptiveThreshold(img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10)
```
- Why: Useful when the CAPTCHA has uneven lighting or shadows. This method keeps letters clear even when brightness varies.

7. Morphological Opening (Refer to ocr/preprocess.py)
```bash
$ cv2.morphologyEx(img_array, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
```
- Why: Removes tiny background dots and smooths the text region. Keeps only important character strokes.

8. Upscaling Image Before OCR (Refer to ocr/reader.py)
```bash
$ scaled = processed.resize((w * 3, h * 3))
```
- Why: Larger images allow EasyOCR to detect fine character details that would otherwise be missed.

