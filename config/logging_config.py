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
                
                # extracting status
                status = None
                if isinstance(result, dict):
                    status = result.get("status")
                    #check if result contains status values in values (for category-mapped responses)
                    if not status and any(isinstance(v, str) and v in ("done", "not found", "already exists", "category not found", "spreadsheet not found", "worksheet not found") for v in result.values()):
                        #result here is category-mapped response
                        done_count = sum(1 for v in result.values() if v == "done")
                        total_count = len(result)
                        status = f"partial" if done_count > 0 and done_count < total_count else ("done" if done_count == total_count else "failed")
                elif isinstance(result, str):
                    # result here is a status string
                    status = result

                if status in ("done", "created", "inserted", "deleted", "exists", "found"):
                    logger.info(f"tool succeeded | status={status} | name: {func.__name__} | call args: {kwargs if kwargs else None}")
                elif status == "partial":
                    logger.info(f"tool partially succeeded | status={status} | name: {func.__name__} | call args: {kwargs if kwargs else None}")
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
