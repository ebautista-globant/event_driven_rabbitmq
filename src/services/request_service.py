from src.errors.errors import RequeueError
from src.services.base_transformer import BaseTransformer
import requests


class RequestService:

    def __init__(self, body: dict, message) -> None:
        self.body = body
        self.message = message

    def execute(self):

        if self.body:
            response = requests.get("http://127.0.0.1:8000/inventory/1")

            transformer = BaseTransformer(response.json())
            transformed_data = transformer.execute()

            create_data_response = requests.post("http://127.0.0.1:8000/data_warehouse", json=transformed_data)
        else:
            raise RequeueError(
                message="emtpy_body",
                code=400,
                additional="Request body is not valid or it's empty"
            )
