from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI(title="Hub Solidario - Portal de Gestao")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Estado em memoria para demonstracao de testes E2E
campanhas_db: List[dict] = [
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


class LoginRequest(BaseModel):
    email: str
    senha: str


class CampanhaCreateRequest(BaseModel):
    titulo: str = Field(min_length=3)
    meta: str
    categoria: str


@app.get("/", response_class=HTMLResponse)
async def rota_raiz():
    return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def pagina_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@app.post("/api/login")
async def processar_login(dados: LoginRequest):
    if dados.email == "coordenador@hubsolidario.org" and dados.senha == "Solidario@2026":
        return {"status": "ok", "mensagem": "Autenticado com sucesso", "redirect": "/campanhas"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais invalidas. Verifique seu e-mail e senha.",
    )


@app.get("/campanhas", response_class=HTMLResponse)
async def pagina_campanhas(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="campanhas.html",
        context={"campanhas": campanhas_db},
    )


@app.get("/api/campanhas")
async def listar_campanhas(termo: Optional[str] = None):
    if termo:
        termo_lower = termo.lower()
        return [c for c in campanhas_db if termo_lower in c["titulo"].lower()]
    return campanhas_db


@app.post("/api/campanhas", status_code=status.HTTP_201_CREATED)
async def criar_campanha(dados: CampanhaCreateRequest):
    if not dados.titulo.strip() or not dados.meta.strip() or not dados.categoria.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preencha todos os campos obrigatorios.",
        )

    try:
        valor_meta = float(dados.meta)
        if valor_meta <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A meta financeira deve ser maior que zero.",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valor da meta financeira invalido.",
        )

    nova_campanha = {
        "id": str(len(campanhas_db) + 1),
        "titulo": dados.titulo.strip(),
        "meta": f"{valor_meta:.2f}",
        "categoria": dados.categoria.strip(),
        "arrecadado": "0.00",
    }
    campanhas_db.append(nova_campanha)
    return nova_campanha
