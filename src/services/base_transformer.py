class BaseTransformer:

    def __init__(self, body):
        self.body = body

    def execute(self):
        return {
            "data": {
                "resource_id": 1,
                "source": "meli",
                "topic": "inventory",
                "processor": "realtime",
                "updated_at": "fake_date",
                "resource_data": self.body
            }
        }
