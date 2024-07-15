import logging


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[37m",  # white
        logging.INFO: "\033[36m",  # cyan
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",  # red
        logging.CRITICAL: "\033[41m",  # white on red bg
    }
    RESET = "\033[0m"
    FORMAT = "%(levelname)s: %(message)s"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = color + record.levelname + self.RESET
        return logging.Formatter(self.FORMAT).format(record)


def init_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
