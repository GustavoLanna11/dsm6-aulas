# Quiz de Programação

Aplicação web de quiz com gamificação (XP + Níveis) para ensino de programação.
Projeto didático para aula sobre **Pirâmide de Testes** e **CI/CD**.

## Stack

- **Backend**: FastAPI + Jinja2 + SQLAlchemy + SQLite
- **Frontend**: HTML/CSS puro
- **Testes**: pytest + Playwright

---


## Setup

### Instalar UV via PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

```

### Opção 1: Com uv

```bash
uv sync --all-extras
uv run playwright install chromium
```

### Opção 2: Com pip

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

---

## Rodar a aplicação

### Com uv

```bash
uv run uvicorn app.main:app --reload
```

### Com pip (venv ativado)

```bash
uvicorn app.main:app --reload
```

Acesse http://localhost:8000

---

## Testes

### Com uv

```bash
# Unitários (base da pirâmide)
uv run pytest tests/test_unit.py -v

# Integração (meio da pirâmide)
uv run pytest tests/test_integration.py -v

# E2E - headless (topo da pirâmide)
uv run pytest tests/test_ui.py -v

# Todos de uma vez
uv run pytest -v
```

### Com pip (venv ativado)

```bash
# Unitários (base da pirâmide)
pytest tests/test_unit.py -v

# Integração (meio da pirâmide)
pytest tests/test_integration.py -v
uv 
# E2E - headless (topo da pirâmide)
pytest tests/test_ui.py -v

# Todos de uma vez
pytest -v
```

### E2E com browser visível

```powershell
# Com pip (venv ativado)
$env:HEADED="1"; pytest tests/test_ui.py -v

# Com uv
$env:HEADED="1"; uv run pytest tests/test_ui.py -v
```

Ou alterar as variáveis no .env

---

## Docker Compose

A maneira mais simples de rodar e testar a aplicação em um ambiente isolado é usando o **Docker Compose**.

### Como iniciar a aplicação

```bash
# Iniciar a aplicação em segundo plano (background)
docker compose up -d

# Se você alterou o código e deseja reconstruir a imagem:
docker compose up -d --build
```

Acesse a aplicação no navegador em: **http://localhost:8000**

### Como pausar/parar

* **Para parar e remover o container**:
  ```bash
  docker compose down
  ```
* **Para ver os logs do servidor**:
  ```bash
  docker compose logs -f
  ```

### Executar os testes dentro do container Docker

Com o container em execução, você pode rodar **toda a suíte de testes** (unitários, integração e E2E headless) diretamente pelo Compose:

```bash
docker compose exec app pytest -v
```
