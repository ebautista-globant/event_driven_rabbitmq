import os
from dotenv import load_dotenv

load_dotenv()

celery_broker_url = os.environ.get("CELERY_BROKER_URL")
app_env = os.environ.get("APP_ENV")
log_level = os.environ.get("LOG_LEVEL")
