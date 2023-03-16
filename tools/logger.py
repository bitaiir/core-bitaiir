# Imports
import logging


class Logger:

    def __init__(self, user, log_name="log.log", level="debug"):
        # Vars;
        self.user = user
        self.log_name = log_name
        self.level = level

    def print_logger(self, message_type, message):
        # Objects;
        logger = logging.getLogger(self.user)
        handler = logging.FileHandler(self.log_name)

        # Verify levels;
        if self.level == "debug":
            logger.setLevel(logging.DEBUG)
        elif self.level == "info":
            logger.setLevel(logging.INFO)
        elif self.level == "warning":
            logger.setLevel(logging.WARNING)
        elif self.level == "error":
            logger.setLevel(logging.ERROR)
        elif self.level == "critical":
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(logging.INFO)

        # Configure logging;
        log_format = "%(asctime)s - [ %(name)s ] - ( %(levelname)s ): %(message)s"
        logging.basicConfig(format=log_format,
                            datefmt="%Y-%m-%d %H:%M:%S")

        # Configure handler;
        format_logging = logging.Formatter(log_format)
        handler.setFormatter(format_logging)
        logger.addHandler(handler)

        # Print logger;
        if message_type == "debug":
            logger.debug(message)
        elif message_type == "info":
            logger.info(message)
        elif message_type == "warning":
            logger.warning(message)
        elif message_type == "error":
            logger.error(message)
        elif message_type == "critical":
            logger.critical(message)
        else:
            logger.info(message)
