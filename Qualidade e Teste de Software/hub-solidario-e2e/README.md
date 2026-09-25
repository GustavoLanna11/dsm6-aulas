# Hub Solidário - Suíte de Testes E2E com Playwright

Projeto de referência para automação de testes End-to-End (E2E) com **Playwright**, estruturado segundo o padrão **Page Object Model (POM)** e integrado com a aplicação web FastAPI.

---

## Estrutura do Projeto

```text
hub-solidario-e2e/
├── app/
│   ├── __init__.py
│   ├── main.py               # Aplicacao FastAPI servindo telas HTML dinamicas
│   └── templates/
│       ├── login.html        # Interface de login
│       └── campanhas.html    # Painel de campanhas solidarias
├── pages/
│   ├── __init__.py
│   ├── base_page.py          # Page Object base
│   ├── login_page.py         # Page Object da tela de login
│   └── campanhas_page.py     # Page Object do painel de campanhas
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Fixtures do Pytest e servidor de teste automatico
│   ├── test_login_e2e.py     # Testes E2E de login
│   ├── test_campanhas_e2e.py # Testes E2E de campanhas
│   └── test_navegacao_usuario_ia.py # Testes E2E de jornada completa
├── pyproject.toml
└── README.md
```

---

## Como Executar

### 1. Sincronizar Dependências com o `uv`

```bash
uv sync
```

### 2. Instalar o Navegador Chromium

```bash
uv run playwright install chromium
```

### 3. Executar os Testes E2E em Modo Headless

```bash
uv run pytest -m e2e -v
```

### 4. Executar os Testes com Interface Gráfica (*Headed*)

```bash
uv run pytest -m e2e --headed
```

### 5. Iniciar a Aplicação Manualmente para Uso com o Codegen

```bash
uv run uvicorn app.main:app --port 8000 --reload
```

Em outro terminal:

```bash
uv run playwright codegen http://localhost:8000
```
