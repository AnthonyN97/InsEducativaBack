from locust import HttpUser, task

class WebsiteUser(HttpUser):
    @task
    def post_notaPromId(self):
        self.client.post("/notaPromId", json={
            "id_estudiante": "f629bae1-8df1-460a-bcbe-29ba8418f5c1"
        })