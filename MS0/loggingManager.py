import logzero
from logzero import logger
import time

class LoggingManager():

    def __init__(self, instanceId):
        self.instanceId = instanceId
        logzero.logfile("/tmp/rotating-logfile.log", maxBytes=1e6, backupCount=3, disableStderrLogger=True)
        logger.info("{0} started logging".format(self.instanceId))

    def logError(self, message):
        logger.error(self.instanceId + ": " + message)

    def logInfo(self, message):
        logger.info(self.instanceId + ": " + message)