from loguru import logger
import sys


logger.remove(0)
logger.level("INFO", color="<blue>")
logger.level("WARNING", color="<yellow>")
logger.level("ERROR", color="<red>")
logger.level("CRITICAL", color="<RED><bold>")
logger.level("DEBUG", color="<magenta>")

logger.add(
    sys.stdout,
    level="DEBUG",
    format="<cyan>{time:YYYY-MM-DD HH:mm:ss.SSS}</cyan> | <level>{level}</level> | <level>{message}</level> | <yellow>{file}</yellow>",
)


logger.add(
    "logs/app.log",
    rotation="100 MB",
    retention="7 days",
    level="DEBUG",
    compression="zip",
)


__all__ = ["logger"]
