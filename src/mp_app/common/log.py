import logging
from logging.handlers import TimedRotatingFileHandler

from rich.console import Console
from rich.logging import RichHandler

from src.mp_app.constants import config


class DefaultFormatter(logging.Formatter):
    """Setup default formatter logging"""

    def format(self, record):
        """Overwrite format of logging and set default value

        Args:
            record (_type_): record logging

        Returns:
            record: record logging
        """
        record.__dict__.setdefault("profile", "SYSTEM")
        return super().format(record)


# Get root logger
logger = logging.getLogger(config.APP_NAME)
logger.setLevel(logging.DEBUG)

# Create handlers
console = Console()
console_handler = RichHandler(console=console, markup=True)
file_handler = TimedRotatingFileHandler(filename=f"{config.LOG_DIR}/app.log", when="D", interval=1, backupCount=10, encoding="utf-8")

# format logging
detailed_formatter = DefaultFormatter(fmt="%(levelname)s - %(profile)s - %(message)s")
detailed_formatter_file = DefaultFormatter(fmt="%(levelname)s - %(profile)s [%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d] - %(message)s")

console_handler.setFormatter(detailed_formatter)
file_handler.setFormatter(detailed_formatter_file)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

if __name__ == "__main__":
    extra_args = {"profile": "Profile 1"}
    logger.info("This is a SYSTEM message")
    logger.debug("This is a debug message", extra=extra_args)
    logger.info("This is a info message", extra=extra_args)
    logger.error("This is an error message", extra=extra_args)
