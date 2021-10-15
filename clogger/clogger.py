import coloredlogs, logging

class CLogger:
    @staticmethod
    def getLogger(name):
        logger = logging.getLogger(name)
        fmt = '%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
        coloredlogs.install(level='DEBUG', logger=logger, fmt = fmt)
        return logger