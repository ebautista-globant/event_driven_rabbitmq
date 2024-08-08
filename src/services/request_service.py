import json

import requests

from src.errors.errors import RequeueError
from src.services.base_transformer import BaseTransformer


class RequestService:

    def __init__(self, body: str, message) -> None:
        self.body = json.loads(body)
        self.message = message

    def execute(self):

        if self.body:
            topic = self.body["topic"]
            resource_id = self.body["resource_id"]
            response = requests.get(f"http://127.0.0.1:8000/{topic}/{resource_id}")

            transformer = BaseTransformer(self.body, response.json())
            transformed_data = transformer.execute()

            requests.post("http://127.0.0.1:8000/data_warehouse", json=transformed_data)
        else:
            raise RequeueError(
                message="emtpy_body",
                code=400,
                additional="Request body is not valid or it's empty"
            )
