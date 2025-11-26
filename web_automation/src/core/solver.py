from src.automation.browser import init_browser, goto, capture_element_screenshot, close_browser
from src.automation.actions import fill_input, click_button, wait
from src.ocr.reader import get_reader, read_captcha_from_file
from src.utils.constants import CAPTCHA_PATH, DEMO_URL
from src.utils.logger import get_logger

logger = get_logger(__name__)

CAPTCHA_IMAGE_SELECTOR = "img[alt='normal captcha example']"
CAPTCHA_INPUT_SELECTOR = "#simple-captcha-field"
SUBMIT_BUTTON_SELECTOR = "button[data-action='demo_action']"


async def solve_captcha(headless=True):
    browser = None
    try:
        browser, page = await init_browser(headless=headless)
        logger.info("Browser started")

        await goto(page, DEMO_URL)
        logger.info("Opened demo page")

        # Capture CAPTCHA image
        await capture_element_screenshot(page, CAPTCHA_IMAGE_SELECTOR, CAPTCHA_PATH)
        logger.info(f"Captcha saved: {CAPTCHA_PATH}")

        # OCR Recognition
        reader = get_reader(gpu=False)
        text = read_captcha_from_file(CAPTCHA_PATH, reader)
        logger.info(f"OCR extracted text: {text}")

        if not text:
            logger.error("OCR failed to decode captcha")
            return False, None

        # Type CAPTCHA
        await fill_input(page, CAPTCHA_INPUT_SELECTOR, text)
        logger.info("Entered captcha")

        # Submit form
        await click_button(page, SUBMIT_BUTTON_SELECTOR)
        logger.info("Clicked submit")

        await wait(2)

        return True, text

    except Exception as e:
        logger.exception("Error during solve")
        return False, None

    finally:
        if browser:
            await close_browser(browser)
            logger.info("Browser closed.")
