import json
import os
import threading
import time
from pathlib import Path

import pytest
import uvicorn

CHALLENGES_PATH = Path(__file__).parent.parent / "app" / "challenges.json"
ANSWER_MAP = {
    c["pergunta"]: c["resposta"]
    for c in json.loads(CHALLENGES_PATH.read_text(encoding="utf-8"))
}


# Carrega .env se existir
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip("'\""))


@pytest.fixture(scope="module")
def base_url():
    from app.main import app

    config = uvicorn.Config(app, host="127.0.0.1", port=8765, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(2)
    yield "http://127.0.0.1:8765"
    server.should_exit = True


@pytest.fixture
def page(base_url):
    from playwright.sync_api import sync_playwright

    headed = os.environ.get("HEADED", "") == "1"
    slow_mo = int(os.environ.get("SLOW_MO", "0"))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed, slow_mo=slow_mo)
        pg = browser.new_page()
        yield pg, base_url
        browser.close()


@pytest.mark.e2e
def test_pagina_carrega(page):
    pg, url = page
    pg.goto(url)
    assert pg.locator("#pergunta").is_visible()
    assert pg.locator("#resposta").is_visible()
    assert pg.locator("#enviar").is_visible()


@pytest.mark.e2e
def test_resposta_correta_mostra_xp(page):
    pg, url = page
    pg.goto(url)
    pergunta = pg.locator("#pergunta").text_content()
    pg.fill("#resposta", ANSWER_MAP[pergunta])
    pg.click("#enviar")
    pg.wait_for_selector("#resultado")
    content = pg.text_content("#resultado")
    assert "XP" in content


@pytest.mark.e2e
def test_resposta_errada_mostra_incorreta(page):
    pg, url = page
    pg.goto(url)
    pg.fill("#resposta", "resposta_impossivel_xyz")
    pg.click("#enviar")
    pg.wait_for_selector("#resultado")
    content = pg.text_content("#resultado")
    assert "Incorreta" in content
