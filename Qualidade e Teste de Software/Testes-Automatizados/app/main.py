import json
import random
import time
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.business import calcular_nivel, calcular_xp, subiu_de_nivel, verificar_resposta
from app.database import Base, engine, get_db
from app.models import Aluno

app = FastAPI(title="Quiz de Programação")

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

CHALLENGES = json.loads((Path(__file__).parent / "challenges.json").read_text(encoding="utf-8"))

Base.metadata.create_all(bind=engine)


def get_or_create_aluno(db: Session) -> Aluno:
    aluno = db.query(Aluno).first()
    if not aluno:
        aluno = Aluno(nome="Aluno 1")
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
    return aluno


@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    aluno = get_or_create_aluno(db)
    desafio = random.choice(CHALLENGES)
    return templates.TemplateResponse(request, "index.html", {
        "desafio": desafio,
        "aluno": aluno,
        "timestamp": time.time(),
    })


@app.post("/responder", response_class=HTMLResponse)
def responder(
    request: Request,
    resposta: str = Form(...),
    desafio_id: int = Form(...),
    timestamp: float = Form(...),
    db: Session = Depends(get_db),
):
    aluno = get_or_create_aluno(db)
    desafio = next((d for d in CHALLENGES if d["id"] == desafio_id), None)

    acertou = False
    xp_ganho = 0
    nivel_subiu = False

    if desafio and verificar_resposta(resposta, desafio["resposta"]):
        acertou = True
        tempo = time.time() - timestamp
        xp_ganho = calcular_xp(tempo)
        xp_antes = aluno.xp
        aluno.xp += xp_ganho
        aluno.nivel = calcular_nivel(aluno.xp)
        nivel_subiu = subiu_de_nivel(xp_antes, aluno.xp)
        db.commit()
        db.refresh(aluno)

    return templates.TemplateResponse(request, "result.html", {
        "acertou": acertou,
        "xp_ganho": xp_ganho,
        "aluno": aluno,
        "nivel_subiu": nivel_subiu,
    })
