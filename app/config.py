import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", "5000"))
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"