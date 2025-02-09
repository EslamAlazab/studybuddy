from locust import HttpUser, task, between


class MyLoadTest(HttpUser):
    wait_time = between(1, 5)  # Time between requests

    @task
    def test_endpoint(self):
        self.client.get("http://127.0.0.1:100/fastapi/async-rooms")

    # @task
    # def test_endpoint(self):
    #     self.client.get("http://127.0.0.1:100/fastapi/rooms")

    # @task
    # def test_endpoint(self):
    #     self.client.get("http://127.0.0.1:100/api/rooms/?format=json")
