from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RESULT_DIR = BASE_DIR / "results"
OUTPUT_DIR = RESULT_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CAPTCHA_PATH = str(OUTPUT_DIR / "captcha.png")

DEMO_URL = "https://2captcha.com/demo/normal"
