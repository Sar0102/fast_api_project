import logging

from pydantic_settings import BaseSettings
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

class SentrySettings(BaseSettings):
    dsn: str = ""
    traces_sample_rate: float = 1.0

    class Config:
        env_prefix = "SENTRY_"
        env_file = ".env"


sentry_config = SentrySettings()

