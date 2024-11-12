from locust import HttpUser, task

class WebsiteUser(HttpUser):
    @task
    def post_notaPromId(self):
        self.client.post("/notaPromId", json={
            "id_estudiante": "6f920817-91ad-4dc4-933e-25a3975071c0"
        })