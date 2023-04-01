import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    WEATHER_URL = os.getenv('WEATHER_URL')
    LOG_FORMAT = os.getenv("LOG_FORMAT") or '%(asctime)s - %(levelname)s - %(message)s \t - %(name)s (%(filename)s).%(funcName)s(%(lineno)d) ' # https://docs.python.org/3/howto/logging.html#changing-the-format-of-displayed-messages
    LOG_LEVEL = os.getenv("LOG_LEVEL") or 'INFO'
    APPNAME = os.getenv("APPNAME") or 'NONE'
    ENV = os.getenv("ENV") or "DEV"
