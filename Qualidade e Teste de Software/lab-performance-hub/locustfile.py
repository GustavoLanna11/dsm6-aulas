from locust import HttpUser, task, between, tag

class UsuarioHubSolidario(HttpUser):
    # Pausa entre ações
    wait_time = between(0.5, 1.5)

    @tag("ineficiente")
    @task
    def testar_matching_ineficiente(self):
        """Simula requisições ao endpoint de matching com validação de SLA 500ms."""
        with self.client.get(
            "/api/v1/matching/ineficiente",
            catch_response=True,
            name="GET /matching/ineficiente"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Status inesperado: {response.status_code}")
                return

            # Validação de Acordo com o Nível de SLA (Máximo de 500ms)
            tempo_resposta = response.elapsed.total_seconds()
            if tempo_resposta > 0.5:
                response.failure(
                    f"Violacao de SLA: tempo de resposta atingiu {tempo_resposta:.3f}s (> 0.5s)" 
                )
            else:
                response.success()

    @tag("otimizado")
    @task
    def testar_matching_otimizado(self):
        """Simula requisições ao endpoint de matching com validação de SLA 500ms."""
        with self.client.get(
            "/api/v1/matching/otimizado",
            catch_response=True,
            name="GET /matching/otimizado"
        ) as response:
            if response.status_code != 200:
                response.failure(f"Status inesperado: {response.status_code}")
                return

            # Validação de Acordo com o Nível de SLA (Máximo de 500ms)
            tempo_resposta = response.elapsed.total_seconds()
            if tempo_resposta > 0.5:
                response.failure(
                    f"Violacao de SLA: tempo de resposta atingiu {tempo_resposta:.3f}s (> 0.5s)" 
                )
            else:
                response.success()