from src.producers.base_producer import CustomRabbitProducer

from src.config.settings import celery_broker_url
from src.config.celery import queues_to_define


class Producer(CustomRabbitProducer):
    def __init__(self):
        super(Producer).__init__(
            celery_broker_url, queues_to_define
        )

    def send(self, *args, **kwargs):
        return self._send(*args, **kwargs)


class ResourceProducer(Producer):
    def send(self, topic: str, data: dict) -> None:
        self._send(routing_key="meli-resource-queue", queue_data=data)
