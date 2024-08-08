from src.consumers.base_consumer import BaseConsumer

from src.services.request_service import RequestService


class ResourceConsumer(BaseConsumer):
    queue_name = "meli-resource-queue"
    route_keys = {
        "ecommerce.meli.resource.inventory": RequestService,
        "ecommerce.meli.resource.products": RequestService,
        "ecommerce.meli.resource.sales": RequestService,
        "ecommerce.meli.resource.*": RequestService,
    }
