from fastapi import FastAPI, HTTPException, status
from app.gateway_pagamento import(
    GatewayPagamentoError,
    GatewayTimeoutError,
    GatewayIndisponivelError
)

from app.schemas import CriarPedidoRequest, Pedido, RespostaProcessamento
from app.service import PedidoService

app = FastAPI(
    title="Serviço de Pedidos",
    description="API para gerenciamento de pedidos e integração com gateway de pagamento.",
    version="1.0.0"
)

service = PedidoService()

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok", "service": "servico-pedidos"}

@app.post("/pedidos", response_model=RespostaProcessamento, status_code=status.HTTP_201_CREATED)
def criar_pedido(payload: CriarPedidoRequest):
    try:
        resultado = service.processar_novo_pedido(payload)
        return resultado

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc

    except GatewayTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Gateway de pagamentos demorou a responder: {exc}"
        ) from exc

    except GatewayIndisponivelError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Servico de pagamentos temporariamente indisponivel: {exc}"
        ) from exc

    except GatewayPagamentoError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha de comunicacao com o gateway financeiro{exc}"
        ) from exc
    
@app.get("/pedidos/{pedido_id}", response_model=Pedido, status_code=status.HTTP_200_OK)
def obter_pedido(pedido_id: str):
    pedido = service.obter_pedido(pedido_id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido com ID {pedido_id} não encontrado."
        )
    return pedido