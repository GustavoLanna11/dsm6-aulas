"""
API do Hub Solidário - Versão Completa para Comparação de Desempenho.
"""

from collections import defaultdict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Hub Solidário - API de Matching",
    description="Serviço para auditoria de eficiência e testes de carga.",
    version="2.0.0"
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
    Algoritmo ingênuo com laços for aninhados que percorrem todas as demandas e habilidades.
    Gera centenas de milhares de repetições desnecessárias que travam a CPU sob carga.
    """
    matches = []
    for voluntario in voluntarios:
        for demanda in demandas:
            habilidades_em_comum = []
            for hab_v in voluntario["habilidades"]:
                for hab_d in demanda["habilidades_requeridas"]:
                    if hab_v == hab_d:
                        habilidades_em_comum.append(hab_v)

            if len(habilidades_em_comum) > 0 and voluntario["cidade"] == demanda["cidade"]:
                matches.append({
                    "voluntario_id": voluntario["id"],
                    "demanda_id": demanda["id"],
                    "score": len(habilidades_em_comum)
                })
    return matches


def calcular_matching_otimizado(voluntarios: list[dict], demandas: list[dict]) -> list[dict]:
    """
    Algoritmo otimizado com pré-indexação por cidade e conjuntos (set).
    Encontra demandas da mesma cidade diretamente e faz interseção de habilidades instantânea.
    """
    # 1. Agrupa as demandas por cidade em um dicionário (tabela hash)
    demandas_por_cidade = defaultdict(list)
    for demanda in demandas:
        demandas_por_cidade[demanda["cidade"]].append({
            "id": demanda["id"],
            "habilidades_set": set(demanda["habilidades_requeridas"])
        })

    matches = []
    # 2. Percorre os voluntários consultando apenas as demandas da mesma cidade
    for voluntario in voluntarios:
        demandas_candidatas = demandas_por_cidade.get(voluntario["cidade"])
        if not demandas_candidatas:
            continue

        hab_voluntario_set = set(voluntario["habilidades"])
        for demanda in demandas_candidatas:
            intersecao = hab_voluntario_set & demanda["habilidades_set"]
            if intersecao:
                matches.append({
                    "voluntario_id": voluntario["id"],
                    "demanda_id": demanda["id"],
                    "score": len(intersecao)
                })
    return matches


@app.get("/api/v1/health")
def healthcheck():
    """Endpoint leve para monitoramento de status da API."""
    return {"status": "ok", "servico": "hub-solidario-matching"}


@app.get("/api/v1/matching/ineficiente", response_model=list[MatchResponse])
def get_matching_ineficiente():
    """Endpoint com a rotina ineficiente da aula 1 (alto consumo de CPU)."""
    return calcular_matching_ineficiente(VOLUNTARIOS, DEMANDAS)


@app.get("/api/v1/matching/otimizado", response_model=list[MatchResponse])
def get_matching_otimizado():
    """Endpoint refatorado para alta performance sob concorrência."""
    return calcular_matching_otimizado(VOLUNTARIOS, DEMANDAS)