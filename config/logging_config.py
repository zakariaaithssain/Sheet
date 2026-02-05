import logging
from config.settings import Settings


def setup_logging(settings: Settings):
    logging.basicConfig(
        level=settings.log_level,
        format= settings.log_format, 
        handlers= settings.log_handlers
    )
