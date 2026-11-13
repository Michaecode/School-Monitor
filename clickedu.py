"""Clickedu browser integration.

The selectors and navigation must be implemented after confirming the
specific school's Clickedu URL and inspecting its login/attendance workflow.
Do not guess selectors or bypass institutional access controls.
"""

from datetime import date

from playwright.async_api import async_playwright

from attendance import Absence


class ClickeduClient:
    def __init__(self, url: str, username: str, password: str, headless: bool = True):
        self.url = url
        self.username = username
        self.password = password
        self.headless = headless

    async def fetch_absences(self, start: date, end: date) -> list[Absence]:
        """Return the signed-in user's absences in the inclusive date range."""
        # Browser setup is ready; the school-specific login and page selectors
        # are deliberately left unimplemented until the portal is identified.
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=self.headless)
            try:
                page = await browser.new_page()
                await page.goto(self.url, wait_until="domcontentloaded")
                raise NotImplementedError(
                    "Clickedu login and attendance selectors are school-specific. "
                    "Configure them after confirming the portal URL and page layout."
                )
            finally:
                await browser.close()
