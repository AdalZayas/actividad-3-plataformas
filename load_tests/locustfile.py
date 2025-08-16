"""
Locustfile para pruebas de carga de Spring PetClinic.

Este archivo define usuarios virtuales que realizan solicitudes GET
contra la API REST de PetClinic. Permite simular cientos o miles de
usuarios concurrentes y medir el tiempo de respuesta del sistema.

Para ejecutarlo instale `locust` y ejecute el comando:

    locust -f tests/load_tests/locustfile.py --headless -u 1000 -r 50 \
      --host=http://localhost:9966/petclinic --run-time 1m

Donde `-u` indica el número de usuarios simultáneos y `-r` la tasa de
generación de nuevos usuarios por segundo. Ajuste estos valores para
reproducir el requisito de "mil personas a la vez realizan una
consulta en menos de cinco segundos".
"""

from locust import HttpUser, task, between


class PetClinicLoadUser(HttpUser):
    # Espera aleatoria entre las solicitudes para simular usuarios reales
    wait_time = between(1, 3)

    @task
    def get_owners(self):
        """Consulta la lista de propietarios para medir tiempos de respuesta."""
        # La ruta debe ser relativa al parámetro --host
        with self.client.get("/api/owners", name="GET /api/owners", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Código de respuesta inesperado: {response.status_code}")
            # Si la respuesta tarda demasiado locust lo registrará automáticamente