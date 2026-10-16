"""
API do Hub Solidário - Laboratório de Desempenho e Testes de Carga.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Hub Solidário - API de Matching",
    description="Serviço para auditoria de eficiência e testes de carga.",
    version="1.0.0"
)

# Cidades e habilidades para montar o cenário de testes
CIDADES = ["Santos", "Sao Vicente", "Praia Grande", "Guaruja", "Cubatao"]
HABILIDADES_DISPONIVEIS = [
    "primeiros-socorros", "cozinha", "direcao", "logistica",
    "triagem", "apoio-psicologico", "eletricista", "costura"
]

# Cria 600 voluntários com dados fixos para que os testes sejam sempre repetíveis
VOLUNTARIOS = [
    {
        "id": i,
        "nome": f"Voluntario {i}",
        "cidade": CIDADES[i % len(CIDADES)],
        "habilidades": [
            HABILIDADES_DISPONIVEIS[(i + j) % len(HABILIDADES_DISPONIVEIS)]
            for j in range(1 + (i % 3))
        ]
    }
    for i in range(1, 601)
]

# Cria 400 demandas com dados fixos para simular a base de dados
DEMANDAS = [
    {
        "id": 1000 + i,
        "titulo": f"Demanda Emergencial {i}",
        "cidade": CIDADES[(i * 3) % len(CIDADES)],
        "habilidades_requeridas": [
            HABILIDADES_DISPONIVEIS[(i + k) % len(HABILIDADES_DISPONIVEIS)]
            for k in range(1 + (i % 2))
        ]
    }
    for i in range(1, 401)
]


class MatchResponse(BaseModel):
    voluntario_id: int
    demanda_id: int
    score: int


def calcular_matching_ineficiente(voluntarios: list[dict], demandas: list[dict]) -> list[dict]:
    """
    Algoritmo gerado por IA com laços for aninhados que percorrem todas as demandas e habilidades.
    Gera centenas de milhares de repetições desnecessárias que travam a CPU sob carga.
    """
    matches = []
    for voluntario in voluntarios:
        for demanda in demandas:
            # Compara as habilidades do voluntário e da demanda uma a uma
            habilidades_em_comum = []
            for hab_v in voluntario["habilidades"]:
                for hab_d in demanda["habilidades_requeridas"]:
                    if hab_v == hab_d:
                        habilidades_em_comum.append(hab_v)

            # Registra o match se houver habilidades em comum na mesma cidade
            if len(habilidades_em_comum) > 0 and voluntario["cidade"] == demanda["cidade"]:
                matches.append({
                    "voluntario_id": voluntario["id"],
                    "demanda_id": demanda["id"],
                    "score": len(habilidades_em_comum)
                })
    return matches


@app.get("/api/v1/health")
def healthcheck():
    """Endpoint leve de monitoramento de status da API."""
    return {"status": "ok", "servico": "hub-solidario-matching"}


@app.get("/api/v1/matching/ineficiente", response_model=list[MatchResponse])
def get_matching_ineficiente():
    """Endpoint que processa a rotina de matching ineficiente."""
    return calcular_matching_ineficiente(VOLUNTARIOS, DEMANDAS)