from logging import getLoggerClass, addLevelName, setLoggerClass, NOTSET, Logger
from logging import FileHandler as BaseFileHandler
import sys
sys.path.append('config/')
from config import log_cfg

MARKET = 5

class TheLogger(getLoggerClass()):
    MARKET = 5
    def __init__(self, name, level=NOTSET):
        super(TheLogger, self).__init__(name, level)
        #Logger.__init__(self, name, level)
        addLevelName(MARKET, 'MARKET')

    def market(self, msg, *args, **kwargs):
        if self.isEnabledFor(MARKET):
            self._log(MARKET, msg, args, **kwargs)


class Deferred_File_Handler(BaseFileHandler):
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self.filename_set = False
        self.log_config = log_cfg
        kwargs['delay'] = True
        BaseFileHandler.__init__(self, '/dev/null', *args, **kwargs)

    def setFilename(self, filename):
        self.filename = filename
        self.filename_set = True

    def _open(self):
        if self._filename_set:
            self.baseFilename = os.path.join(log_cfg['LOG_ROOT'], self.filename)
            return BaseFileHandler._open(self)
