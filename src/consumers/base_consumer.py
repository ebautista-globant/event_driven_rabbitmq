import json

from celery import bootsteps
from kombu import Consumer
from kombu import Queue

from src.config.celery import default_exchange
from src.errors.errors import QueueErrorHandle


class BaseConsumer(bootsteps.ConsumerStep):
    route_keys: dict
    queue_name: str

    @staticmethod
    def parse_body(body):
        if isinstance(body, dict):
            return body
        else:
            return body

    def get_consumers(self, channel):
        queues = []
        for routing, processor in self.route_keys.items():
            queue = Queue(
                self.queue_name,
                default_exchange,
                routing_key=routing,
                queue_arguments={"x-dead-letter-exchange": "celery.error"},
                acks_late=True
            )
            queues.append(queue)

        return [
            Consumer(
                channel,
                queues=queues,
                callbacks=[self.handle_message],
                accept=["json"],
                prefetch_count=5,
            )
        ]

    def handle_message(self, body, message):
        handle = QueueErrorHandle(self)
        with handle.handle_errors():
            key = message.delivery_info.get("routing_key")
            bdy = self.parse_body(body)
            processor = self.route_keys.get(key)
            if processor:
                processor(bdy, message).execute()

            else:
                handle.requeue = 0
                handle.reject = 1
        handle.process_message(message)
