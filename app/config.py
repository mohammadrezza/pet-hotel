import os
from typing import List, Type


class BaseConfig:
    CONFIG_NAME = "base"
    DEBUG = False
    MONGO_URI = ''
    JWT_SECRET_KEY = ''


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    SECRET_KEY = os.getenv("DEV_SECRET_KEY", "how's my security?")
    DEBUG = True
    TESTING = False
    MONGO_URI = 'mongodb://localhost:27017/pet_hotel'
    JWT_SECRET_KEY = 'dev-super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = 1 * 24 * 60 * 60
    SIB_BASE_URL = 'https://api.sendinblue.com/v3/smtp/email'
    SIB_API_KEY = 'YOUR-SEND-IN_BLUE-API-KEY'


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "how's my security?")
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGO_URI = 'mongodb://localhost:27017/test_pet_hotel'
    JWT_SECRET_KEY = 'test-super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = 1 * 24 * 60 * 60


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "how's my security?")
    DEBUG = False
    TESTING = False


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
