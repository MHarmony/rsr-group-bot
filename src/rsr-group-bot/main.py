import logging

from logger.logger import Logger


class RsrGroupBot:
    def __init__(self):
        Logger()

        self.logger = logging.getLogger("logger")


if __name__ == "__main__":
    RsrGroupBot()
