from DataFeed import DataFeed
import sys
import logging
import logging.config
from Logger import TheLogger

sys.path.append('config/')
from config import settings


logging.setLoggerClass(TheLogger)
#print type(settings['Logging'])
#print settings['Logging']['formatters']
log = logging.getLogger('Launcher')
logging.config.dictConfig(settings['Logging'])
log.info('Logger instantiated')
feed = DataFeed(settings['DataFeed'])
feed.recvLoop()


