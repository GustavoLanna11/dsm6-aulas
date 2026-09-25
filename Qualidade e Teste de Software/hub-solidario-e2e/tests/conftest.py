from collections.abc import Generator
import socket
import threading
import time
import pytest
import uvicorn
from app.main import app, campanhas_db


def obter_porta_livre() -> int:
    """Encontra uma porta TCP disponivel para o servidor de teste."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def server_port() -> int:
    return obter_porta_livre()


@pytest.fixture(scope="session")
def server_url(server_port: int) -> Generator[str, None, None]:
    """Inicia o servidor FastAPI em thread de segundo plano durante a sessao de testes."""
    config = uvicorn.Config(app=app, host="127.0.0.1", port=server_port, log_level="warning")
    server = uvicorn.Server(config=config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Aguarda brevemente a estabilizacao do servidor HTTP
    time.sleep(0.5)

    yield f"http://127.0.0.1:{server_port}"

    server.should_exit = True
    thread.join(timeout=2)


@pytest.fixture(autouse=True)
def restaurar_estado_campanhas() -> Generator[None, None, None]:
    """Restaura o estado inicial do banco de dados em memoria antes e apos cada teste."""
    estado_padrao = [
        {
            "id": "1",
            "titulo": "Agasalho Amigo 2026",
            "meta": "20000.00",
            "categoria": "Agasalhos e Cobertores",
            "arrecadado": "12500.00",
        },
        {
            "id": "2",
            "titulo": "Prato Cheio Comunidade",
            "meta": "35000.00",
            "categoria": "Alimentacao",
            "arrecadado": "35000.00",
        },
    ]
    campanhas_db.clear()
    campanhas_db.extend([dict(c) for c in estado_padrao])
    yield
    campanhas_db.clear()
    campanhas_db.extend([dict(c) for c in estado_padrao])
