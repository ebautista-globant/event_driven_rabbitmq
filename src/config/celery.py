from kombu import binding
from kombu import Exchange
from kombu import Queue

default_exchange = Exchange("microservices", type="topic", durable=True)
error_exchange = Exchange("celery.error", type="topic", durable=True)


def queue_definitions_configuration(queue_definitions):
    error_bindings = []
    queues = []

    for definition in queue_definitions:
        queue_bindings = []

        for routing in definition["routings"]:
            queue_bindings.append(
                binding(default_exchange, routing_key=routing)
            )
            error_bindings.append(
                binding(error_exchange, routing_key=routing)
            )

        queue = Queue(
            definition["name"],
            default_exchange,
            bindings=queue_bindings,
            queue_arguments={"x-dead-letter-exchange": "celery.error"},
            acks_late=True,
        )
        queues.append(queue)

    dead_letter_queue = Queue(
        "dead_letter", exchange=error_exchange, bindings=error_bindings
    )
    queues.append(dead_letter_queue)

    return queues


base_queue_definitions = [
    {
        "name": "meli-realtime-queue",
        "routings": ["ecommerce.meli.realtime.*"]
    },
    {
        "name": "meli-historic-queue",
        "routings": ["ecommerce.meli.historic.*"]
    },
    {
        "name": "meli-resource-queue",
        "routings": ["ecommerce.meli.resource.*"]
    }
]

queues_to_define = queue_definitions_configuration(base_queue_definitions)

__all__ = [
    "queues_to_define",
    "default_exchange"
]
