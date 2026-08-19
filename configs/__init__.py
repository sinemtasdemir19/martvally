from .base_config import Config
from .development_config import DevelopmentConfig
from .production_config import ProductionConfig


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}