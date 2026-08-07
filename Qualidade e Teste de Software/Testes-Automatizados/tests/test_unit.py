import pytest

from app.business import calcular_nivel, calcular_xp, subiu_de_nivel, verificar_resposta


@pytest.mark.unit
def test_xp_resposta_rapida():
    assert calcular_xp(3.0) == 100


@pytest.mark.unit
def test_xp_resposta_media():
    assert calcular_xp(10.0) == 50


@pytest.mark.unit
def test_xp_resposta_lenta():
    assert calcular_xp(20.0) == 25


@pytest.mark.unit
def test_xp_limite_5_segundos():
    assert calcular_xp(5.0) == 100


@pytest.mark.unit
def test_xp_limite_15_segundos():
    assert calcular_xp(15.0) == 50


@pytest.mark.unit
def test_resposta_correta():
    assert verificar_resposta("4", "4") is True


@pytest.mark.unit
def test_resposta_incorreta():
    assert verificar_resposta("5", "4") is False


@pytest.mark.unit
def test_resposta_ignora_espacos():
    assert verificar_resposta("  4  ", "4") is True


@pytest.mark.unit
def test_resposta_ignora_maiusculas():
    assert verificar_resposta("Print", "print") is True


@pytest.mark.unit
def test_nivel_inicial():
    assert calcular_nivel(0) == 1


@pytest.mark.unit
def test_nivel_1_com_xp():
    assert calcular_nivel(999) == 1


@pytest.mark.unit
def test_nivel_2():
    assert calcular_nivel(1000) == 2


@pytest.mark.unit
def test_nivel_3():
    assert calcular_nivel(2500) == 3


@pytest.mark.unit
def test_subiu_de_nivel():
    assert subiu_de_nivel(950, 1050) is True


@pytest.mark.unit
def test_nao_subiu_de_nivel():
    assert subiu_de_nivel(100, 200) is False
