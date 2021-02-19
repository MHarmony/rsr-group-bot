import logging
import os

from dotenv import load_dotenv


class Logger:
    def __init__(self):
        load_dotenv()

        self.logLevel = os.getenv("LOG_LEVEL")
        self.logLevelParsed = self.parseLogLevel(self.logLevel)
        self.logLocation = os.getenv("LOG_LOCATION")

        self.setupLogger()

    def parseLogLevel(self, logLevel="DEBUG"):
        logLevels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        return logLevels.get(logLevel)

    def setupLogger(self):
        logger = logging.getLogger("logger")

        fileHandler = logging.FileHandler(self.logLocation, mode="a", delay=True)
        fileHandlerFormat = logging.Formatter(
            "%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fileHandler.setLevel(self.logLevelParsed)
        fileHandler.setFormatter(fileHandlerFormat)

        consoleHandler = logging.StreamHandler()
        consoleHandlerFormat = logging.Formatter(
            "[%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fileHandler.setLevel(self.logLevelParsed)
        consoleHandler.setFormatter(consoleHandlerFormat)

        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)
