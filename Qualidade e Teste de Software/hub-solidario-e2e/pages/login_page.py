from playwright.sync_api import Locator, Page
from pages.base_pages import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.campo_email: Locator = page.get_by_label("E-mail de Acesso")
        self.campo_senha: Locator = page.get_by_label("Senha")
        self.botao_entrar: Locator = get_by_role("button", name="Entrar no Sistema")
        self.alerta_erro: Locator = page.get_by_role("alert")

    def acessar_pagina(self, base_url: str) -> None:
        self.navegar_para(f"{base_url}/login")

    def preencher_credenciais(self, email: str, senha: str) -> None:
        self.campo_email.fill()