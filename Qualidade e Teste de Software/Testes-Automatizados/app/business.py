def calcular_xp(tempo_resposta: float) -> int:
    if tempo_resposta <= 5:
        return 100
    if tempo_resposta <= 15:
        return 50
    return 25


def verificar_resposta(resposta: str, gabarito: str) -> bool:
    return resposta.strip().lower() == gabarito.strip().lower()


def calcular_nivel(xp_total: int) -> int:
    return xp_total // 1000 + 1


def subiu_de_nivel(xp_antes: int, xp_depois: int) -> bool:
    return calcular_nivel(xp_antes) < calcular_nivel(xp_depois)
