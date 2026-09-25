from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def navegar_para(self, url: str) -> None:
        self.page.goto(url)

