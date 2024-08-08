class BaseTransformer:

    def __init__(self, body, response):
        self.body = body
        self.response = response

    def execute(self):
        return {
            "data": {
                "resource_id": self.body["resource_id"],
                "source": self.body["source"],
                "topic": self.body["topic"],
                "processor": self.body["processor"],
                "updated_at": "fake_date",
                "resource_data": self.response
            }
        }
