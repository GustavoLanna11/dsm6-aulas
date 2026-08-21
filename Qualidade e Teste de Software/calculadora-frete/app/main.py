from fastapi import FastAPI, HTTPException, status
from pydantic import basemodel

app = FastAPI(title="Calculadora de Frete Simplificada")

NORTE_UFS = {"AM", "RR", "AP", "PA", "AC", "RO", "TO"}
VALID_UFS = NORTE_UFS.union({
    "AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE", "DF", "GO", "MT", "MS", "ES", "MG", "RJ", "SP", "PR", "RS", "SC"
})

class FreteRequest(BaseModel):
    peso: float
    uf: str

def calcular_frete(peso: float, uf: str) -> float:
    if peso <= 0:
        raise ValueError("O peso deve ser maior que zero")
    if peso > 30:
        raise ValueError("Peso excede o limite máximo permitido de 30kg")
    
    uf_upper = uf.strip().upper()
    if uf_upper not in VALID_UFS:
        raise ValueError("UF inválida")

    if peso <= 10.0:
        valor_base = 20.0