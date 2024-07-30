from celery import Celery

from src.consumers.realtime_consumer import RealtimeConsumer
from src.consumers.historic_consumer import HistoricConsumer
from src.consumers.resource_consumer import ResourceConsumer

app = Celery("app")
app.conf.update(
    enable_utc=True,
    timezone="America/Mexico_City",
    worker_log_format="%(message)s",
    broker_connection_retry_on_startup=True,
)

app.steps["consumer"].add(RealtimeConsumer)
app.steps["consumer"].add(HistoricConsumer)
app.steps["consumer"].add(ResourceConsumer)
