import asyncio
from playwright.async_api import async_playwright

async def main():
    print("Starting...")
    p = await async_playwright().start()
    print("Playwright Started")

    browser = await p.chromium.launch(headless=True)
    print("Browser Launched")

    page = await browser.new_page()
    await page.goto("https://google.com")
    print(await page.title())

    await browser.close()
    await p.stop()

asyncio.run(main())