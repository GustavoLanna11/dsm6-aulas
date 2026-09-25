import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

@pytest.mark.e2e
def test_login_com_credenciais_validas_redireciona_para_painel(page: Page, server_url: str):
    """ VALIDA O FLUXO DE AUTENTICAÇÃO COM SUCESSO """

    #Arrange
    login_page = LoginPage(page)
    login_page.acessar_pagina(server_url)

    #Act
    login_page.realizar_login_completo("coordenador@hubsolidario.org", "Solidario@2026")

    #Assert
    expect(page.get_by_role("heading", name="Painel de Campanhas")).to_be_visible()

def test_login_com_credenciais_invalidas_exibe_mensagem_de_alerta(page: Page, server_url: str):
    """ Valida que credenciais incorretas disparam alerta de erro """

    #Arrange
    login_page = LoginPage(page)
    login_page.acessar_pagina(server_url)

    #Act
    login_page.realizar_login_completo("")