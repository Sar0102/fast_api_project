import sentry_sdk
import uvicorn
from app import create_app
from infrastructure.loging_configs.sentry import sentry_config

if __name__ == "__main__":
    # sentry_sdk.init(**sentry_config.model_dump())
    app = create_app()
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
