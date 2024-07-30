import json

from kombu import Connection
from kombu import Producer


class CustomRabbitProducer:
    producer: Producer

    def __init__(self, celery_broker_url: str, queues: list):
        self.connection = Connection(celery_broker_url)
        self.producer = self.connection.Producer()
        self.queues = queues

    def _send(
            self,
            routing_key: str,
            queue_data: dict,
            exchange="microservices",
    ):
        self.producer.publish(
            exchange=exchange,
            declare=self.queues,
            routing_key=routing_key,
            body=json.dumps(queue_data),
            content_type="application/json",
            retry=True,
            retry_policy={
                "interval_start": 0,
                "interval_step": 2,
                "interval_max": 30,
                "max_retries": 30,
            }
        )
