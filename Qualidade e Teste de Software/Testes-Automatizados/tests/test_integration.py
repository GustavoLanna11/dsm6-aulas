import time

import pytest


@pytest.mark.integration
def test_pagina_inicial_carrega(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Desafio" in response.text


@pytest.mark.integration
def test_resposta_correta_ganha_xp(client):
    response = client.post("/responder", data={
        "resposta": "4",
        "desafio_id": 1,
        "timestamp": str(time.time()),
    })
    assert response.status_code == 200
    assert "Correta" in response.text
    assert "XP" in response.text


@pytest.mark.integration
def test_resposta_errada_nao_ganha_xp(client):
    response = client.post("/responder", data={
        "resposta": "999",
        "desafio_id": 1,
        "timestamp": str(time.time()),
    })
    assert response.status_code == 200
    assert "Incorreta" in response.text
