from src.consumers.base_consumer import BaseConsumer

from src.services.request_service import RequestService


class RealtimeConsumer(BaseConsumer):
    queue_name = "meli-realtime-queue"
    route_keys = {
        "ecommerce.meli.realtime.inventory": RequestService,
        "ecommerce.meli.realtime.products": RequestService,
        "ecommerce.meli.realtime.sales": RequestService,
        "ecommerce.meli.realtime.*": RequestService,
    }
