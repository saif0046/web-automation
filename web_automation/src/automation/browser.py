from pyppeteer import launch


async def init_browser(headless: bool = False):
    """
    Launch a new Chromium browser instance.
    """
    browser = await launch(
        headless=headless,
        executablePath=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage'
        ]
    )
    page = (await browser.pages())[0]
    return browser, page


async def goto(page, url: str, wait_until: str = "networkidle2"):
    """
    Navigate the browser to a target URL.
    """
    await page.goto(url, {"waitUntil": wait_until})


async def capture_element_screenshot(page, selector: str, output_path: str, timeout: int = 5000):
    """
    Capture a screenshot of an element (CAPTCHA image).
    """
    await page.waitForSelector(selector, {"timeout": timeout})
    el = await page.querySelector(selector)
    if el is None:
        raise RuntimeError(f"Selector not found: {selector}")
    await el.screenshot({"path": output_path})
    return output_path


async def close_browser(browser):
    """
    Safely close the browser instance.
    """
    try:
        await browser.close()
    except Exception:
        pass
