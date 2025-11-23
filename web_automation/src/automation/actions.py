"""
UI Interaction Module
---------------------
Handles user-like interactions such as typing and clicking inside the page.
"""

async def fill_input(page, selector: str, text: str, timeout: int = 5000):
    """
    Type text inside an input field.
    """
    await page.waitForSelector(selector, {"timeout": timeout})

    # Clear existing value
    await page.evaluate(f"document.querySelector('{selector}').value = ''")

    await page.type(selector, text)


async def click_button(page, selector: str, timeout: int = 5000):
    """
    click a button
    """
    await page.waitForSelector(selector, {"timeout": timeout})
    await page.click(selector)


async def wait(seconds: float):
    """
    Simple async sleep.
    """
    import asyncio
    await asyncio.sleep(seconds)
