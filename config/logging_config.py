import logging.config
import functools
import logging


#decorator to facilitate tools logging
def log_tool(logger: logging.Logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(
                f"Tool called. name: {func.__name__}, call args: {kwargs if kwargs else None}")
            try:
                result = func(*args, **kwargs)
                status = result.get("status") if isinstance(result, dict) else None

                if status in ("done", "created", "inserted", "deleted", "exists", "found"):
                    logger.info(f"tool succeeded | status={status} | name: {func.__name__} | call args: {kwargs if kwargs else None}")
                elif status:
                    logger.warning(f"tool completed with status={status} | name: {func.__name__} | call args: {kwargs if kwargs else None}")

                return result

            except Exception:
                logger.error("tool failed", exc_info=True)
                raise
        return wrapper
    return decorator


def setup_logging(settings):
    "set up logging config"
    logging.config.dictConfig(settings.log_config)
