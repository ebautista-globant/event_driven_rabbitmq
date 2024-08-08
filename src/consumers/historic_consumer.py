from src.consumers.base_consumer import BaseConsumer

from src.services.request_service import RequestService


class HistoricConsumer(BaseConsumer):
    queue_name = "meli-historic-queue"
    route_keys = {
        "ecommerce.meli.historic.inventory": RequestService,
        "ecommerce.meli.historic.products": RequestService,
        "ecommerce.meli.historic.sales": RequestService,
        "ecommerce.meli.historic.*": RequestService,
    }
