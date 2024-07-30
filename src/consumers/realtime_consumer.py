from src.consumers.base_consumer import BaseConsumer

from src.services.request_service import RequestService


class RealtimeConsumer(BaseConsumer):
    route_keys = {
        "ecommerce.meli.realtime.sales": RequestService,
        "ecommerce.meli.realtime.products": RequestService,
        "ecommerce.meli.realtime.inventory": RequestService,
    }
    queue_name = "meli-realtime-queue"
