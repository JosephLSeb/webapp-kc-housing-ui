from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(3, 4)

    @task
    def home(self):
        self.client.get("/")
    
    @task
    def analysis(self):
        data = {
            "bedrooms": 7,
            "price_range": 3
            
        }
        self.client.post("/analysis", data=data)