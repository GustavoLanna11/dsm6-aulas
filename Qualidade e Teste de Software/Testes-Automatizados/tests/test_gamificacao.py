"""
Suite de testes unitários — Motor de Gamificação
Cobre: calcular_xp, calcular_nivel e subiu_de_nivel
"""

import pytest

from app.business import calcular_nivel, calcular_xp, subiu_de_nivel


# ---------------------------------------------------------------------------
# calcular_xp — faixas de tempo
# ---------------------------------------------------------------------------

class TestCalcularXP:

    # --- faixa rápida (≤ 5 s) → 100 XP ---

    def test_xp_tempo_zero(self):
        """Tempo zero (resposta instantânea) deve conceder 100 XP."""
        assert calcular_xp(0.0) == 100

    def test_xp_tempo_muito_rapido(self):
        """Tempo bem abaixo do limite rápido deve conceder 100 XP."""
        assert calcular_xp(1.0) == 100

    def test_xp_exatamente_no_limite_rapido(self):
        """Exatamente 5 s é inclusivo na faixa rápida → 100 XP."""
        assert calcular_xp(5.0) == 100

    def test_xp_logo_apos_limite_rapido(self):
        """5.001 s já cai na faixa média → 50 XP."""
        assert calcular_xp(5.001) == 50

    # --- faixa média (> 5 s e ≤ 15 s) → 50 XP ---

    def test_xp_faixa_media_inicio(self):
        """Primeiro valor inteiro acima de 5 s deve conceder 50 XP."""
        assert calcular_xp(6.0) == 50

    def test_xp_faixa_media_meio(self):
        """Valor no meio da faixa média deve conceder 50 XP."""
        assert calcular_xp(10.0) == 50

    def test_xp_exatamente_no_limite_medio(self):
        """Exatamente 15 s é inclusivo na faixa média → 50 XP."""
        assert calcular_xp(15.0) == 50

    def test_xp_logo_apos_limite_medio(self):
        """15.001 s já cai na faixa lenta → 25 XP."""
        assert calcular_xp(15.001) == 25

    # --- faixa lenta (> 15 s) → 25 XP ---

    def test_xp_faixa_lenta_inicio(self):
        """Primeiro valor inteiro acima de 15 s deve conceder 25 XP."""
        assert calcular_xp(16.0) == 25

    def test_xp_faixa_lenta_valor_alto(self):
        """Tempo muito alto (ex.: 300 s) ainda deve conceder 25 XP."""
        assert calcular_xp(300.0) == 25

    # --- tipo de retorno ---

    def test_xp_retorna_inteiro(self):
        """calcular_xp deve sempre retornar int."""
        assert isinstance(calcular_xp(3.0), int)
        assert isinstance(calcular_xp(10.0), int)
        assert isinstance(calcular_xp(20.0), int)

    # --- valores de XP possíveis ---

    def test_xp_so_retorna_valores_validos(self):
        """Os únicos valores possíveis de XP são 25, 50 ou 100."""
        tempos = [0, 1, 5, 5.001, 10, 15, 15.001, 60, 120]
        for t in tempos:
            assert calcular_xp(t) in (25, 50, 100), (
                f"calcular_xp({t}) retornou valor inesperado"
            )


# ---------------------------------------------------------------------------
# calcular_nivel — progressão de nível
# ---------------------------------------------------------------------------

class TestCalcularNivel:

    def test_nivel_com_xp_zero(self):
        """Com 0 XP o jogador está no nível 1."""
        assert calcular_nivel(0) == 1

    def test_nivel_antes_do_primeiro_threshold(self):
        """999 XP ainda é nível 1."""
        assert calcular_nivel(999) == 1

    def test_nivel_exatamente_no_primeiro_threshold(self):
        """1000 XP marca a entrada no nível 2."""
        assert calcular_nivel(1000) == 2

    def test_nivel_dentro_do_segundo_threshold(self):
        """1500 XP continua no nível 2."""
        assert calcular_nivel(1500) == 2

    def test_nivel_no_segundo_threshold_exato(self):
        """1999 XP ainda é nível 2."""
        assert calcular_nivel(1999) == 2

    def test_nivel_exatamente_no_terceiro_threshold(self):
        """2000 XP marca a entrada no nível 3."""
        assert calcular_nivel(2000) == 3

    def test_nivel_alto(self):
        """10 000 XP deve resultar em nível 11."""
        assert calcular_nivel(10_000) == 11

    def test_nivel_muito_alto(self):
        """100 000 XP deve resultar em nível 101."""
        assert calcular_nivel(100_000) == 101

    def test_nivel_retorna_inteiro(self):
        """calcular_nivel deve sempre retornar int."""
        assert isinstance(calcular_nivel(0), int)
        assert isinstance(calcular_nivel(1500), int)

    def test_nivel_formula_consistente(self):
        """Verifica a fórmula xp // 1000 + 1 para uma sequência de valores."""
        for xp in range(0, 5001, 100):
            esperado = xp // 1000 + 1
            assert calcular_nivel(xp) == esperado, (
                f"calcular_nivel({xp}) deveria ser {esperado}"
            )


# ---------------------------------------------------------------------------
# subiu_de_nivel — detecção de subida de nível
# ---------------------------------------------------------------------------

class TestSubiuDeNivel:

    # --- casos que NÃO geram subida ---

    def test_sem_ganho_de_xp(self):
        """Nenhum XP ganho: não sobe de nível."""
        assert subiu_de_nivel(500, 500) is False

    def test_ganho_dentro_do_mesmo_nivel(self):
        """Ganho que permanece no nível 1 não deve reportar subida."""
        assert subiu_de_nivel(0, 999) is False

    def test_ganho_que_nao_cruza_threshold(self):
        """Ganho dentro do nível 2 não deve reportar subida."""
        assert subiu_de_nivel(1000, 1999) is False

    def test_xp_antes_e_depois_iguais_nivel_alto(self):
        """XP inalterado em nível alto não deve reportar subida."""
        assert subiu_de_nivel(5000, 5000) is False

    # --- casos que GERAM subida ---

    def test_cruzamento_do_nivel_2(self):
        """Cruzar 1000 XP deve detectar subida para o nível 2."""
        assert subiu_de_nivel(950, 1050) is True

    def test_cruzamento_do_nivel_3(self):
        """Cruzar 2000 XP deve detectar subida para o nível 3."""
        assert subiu_de_nivel(1900, 2100) is True

    def test_cruzamento_do_nivel_5(self):
        """Cruzar 4000 XP deve detectar subida para o nível 5."""
        assert subiu_de_nivel(3800, 4100) is True

    def test_subida_exatamente_no_threshold(self):
        """xp_antes=999, xp_depois=1000 deve detectar subida."""
        assert subiu_de_nivel(999, 1000) is True

    # --- salto de múltiplos níveis ---

    def test_salto_de_multiplos_niveis(self):
        """Ganho de XP que pula mais de um nível deve ser detectado."""
        assert subiu_de_nivel(0, 3000) is True

    def test_salto_do_nivel_1_ao_nivel_11(self):
        """Salto de 0 a 10 000 XP deve ser detectado como subida."""
        assert subiu_de_nivel(0, 10_000) is True

    # --- combinação calcular_xp + subiu_de_nivel ---

    def test_xp_rapido_cruza_nivel_2(self):
        """Ganhar 100 XP rápidos com 950 XP iniciais deve subir para nível 2."""
        xp_ganho = calcular_xp(3.0)          # 100 XP
        assert subiu_de_nivel(950, 950 + xp_ganho) is True

    def test_xp_lento_nao_cruza_nivel(self):
        """Ganhar 25 XP lentos com 100 XP iniciais não deve subir de nível."""
        xp_ganho = calcular_xp(60.0)         # 25 XP
        assert subiu_de_nivel(100, 100 + xp_ganho) is False

    def test_xp_medio_cruza_nivel_quando_proximo_do_threshold(self):
        """Ganhar 50 XP médios com 960 XP iniciais não cruza 1000 → sem subida."""
        xp_ganho = calcular_xp(10.0)         # 50 XP
        assert subiu_de_nivel(960, 960 + xp_ganho) is False

    def test_xp_rapido_exatamente_no_threshold(self):
        """900 XP + 100 XP rápidos = 1000 XP exatos → sobe para nível 2."""
        xp_ganho = calcular_xp(1.0)          # 100 XP
        assert subiu_de_nivel(900, 900 + xp_ganho) is True

    # --- tipo de retorno ---

    def test_subiu_retorna_bool(self):
        """subiu_de_nivel deve sempre retornar bool."""
        assert isinstance(subiu_de_nivel(0, 500), bool)
        assert isinstance(subiu_de_nivel(900, 1100), bool)
