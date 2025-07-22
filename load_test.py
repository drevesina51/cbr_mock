from locust import HttpUser, task, between

class CBRUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task
    def get_rates(self):
        test_id = self.client.base_url.split("//")[1].replace(".", "_")
        self.client.get(
            "/scripts/XML_daily.asp",
            params={"date_req": "22/07/2025", "test_id": test_id}
        )
    
    @task(3)
    def healthcheck(self):
        self.client.get("/healthcheck")
