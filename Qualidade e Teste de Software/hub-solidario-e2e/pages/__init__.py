"""Pacote contendo os Page Objects da aplicacao Hub Solidario."""
from pages.base_page import BasePage
from pages.campanhas_page import CampanhasPage
from pages.login_page import LoginPage

__all__ = ["BasePage", "LoginPage", "CampanhasPage"]
