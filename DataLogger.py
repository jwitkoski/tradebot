from Logger import TheLogger, Deferred_File_Handler
from logging import Formatter, StreamHandler
from Queue import Queue


#Class that will be used for logging market updates on subbed order pairs
class DataLogger:
    def __init__(self, pairs, messages, logging=False):
        self.market_fmt = Formatter('[%(asctime)s] %(name)s -%(levelname)s - %(message)s','%d/%m/%Y - %H:%M:%S')
        self.ch = StreamHandler()
        self.ch.setLevel(TheLogger.MARKET)
        self.ch.setFormatter(self.market_fmt)
        self.dfh = Deferred_File_Handler('tmp.log')
        self.dfh.setLevel(TheLogger.MARKET)
        self.dfh.setFormatter(self.market_fmt)
        self.logging = logging
        if logging:
            self.log_dict = {}
            for pair in pairs:
                for msg in messages:
                    if msg not in ['error','subscriptions']:
                        self.log_dict[msg][pair] = TheLogger.getLogger(' - '.join([msg, pair]))
                        self.log_dict[msg][pair].setLevel(TheLogger.MARKET)
                        self.dfh.setFilename('market/%s_%s.log'%(msg, pair))
                        self.log_dict[msg][pair].addHandler(self.dfh)
                        self.log_dict[msg][pair].addHandler(self.ch)

    def log(self, msg):
        if self.logging:
            self.log_dict[msg['type']][msg['product_id']].market(msg)
