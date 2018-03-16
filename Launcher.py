from gdax_client import GdaxClient
import sys
import logging
import logging.config
from Logger import Logger_

sys.path.append('config/')
from config import settings



logging.setLoggerClass(Logger_)
#print type(settings['Logging'])
#print settings['Logging']['formatters']
log = logging.getLogger('Launcher')
logging.config.dictConfig(settings['Logging'])
log.info('Initialized Logger!')
client = GdaxClient()

