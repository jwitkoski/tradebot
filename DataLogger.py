from Logger import Logger_, Deferred_File_Handler
from logging import getLogger, DEBUG
from logging import Formatter, StreamHandler, FileHandler
import Queue


#Class that will be used for logging market updates on subbed order pairs
class DataLogger:
    def __init__(self, pairs, messages, logging=False):
        self._log = getLogger('DataLogger')
        self.logging = logging
        self.last_seqNum = 0
        if logging:
            self._qlog_dict = {}
            for pair in pairs:
                for msg in messages:
                    if msg not in ['error','subscriptions']:
                        self._log.debug('Creating (Queue, Logger) tuple for %s - %s' %(msg,pair))
                        if msg in ['l2update', 'snapshot']:
                            self._qlog_dict[(msg, pair)] = [Queue.Queue(), self.setupLogger(msg, pair)]
                        else:
                            self._qlog_dict[(msg, pair)] = [Queue.PriorityQueue(), self.setupLogger(msg, pair)]
                        #self._qlog_dict[(msg, pair)][1].setLevel(Logger_.MARKET)
                        #self.dfh.setFilename('market/%s_%s.log'%(msg, pair))
                        #self._qlog_dict[(msg, pair)][1].addHandler(self.dfh)
                        #self._qlog_dict[(msg, pair)][1].addHandler(self.ch)
        self._log.debug('Initialized DataLogger!')

    def setupLogger(self, msg, pair):
        market_fmt = Formatter('[%(asctime)s] %(name)s - %(message)s','%d/%m/%Y - %H:%M:%S')
        ch = StreamHandler()
        ch.setLevel(DEBUG)
        ch.setFormatter(market_fmt)
        dfh = Deferred_File_Handler('market/%s_%s.log' %(msg, pair))
        dfh.setLevel(Logger_.MARKET)
        dfh.setFormatter(market_fmt)
        log = getLogger(' - '.join([msg, pair]))
        log.setLevel(Logger_.MARKET)
        log.addHandler(dfh)
        log.addHandler(ch)
        return log

    def _handleq(self, type_, id_):
        seqNum = 0
        self._log.info('Dumping Queue for %s - %s' %(type_, id_))
        if type_ in ['l2update','snapshot']:
            while not self._qlog_dict[(type_, id_)][0].empty():
                msg = self._qlog_dict[(type_, id_)][0].get()
                if self.logging:
                    self._qlog_dict[(type_, id_)][1].market(msg)
                    #self._qlog_dict[(type_, id_)][1].debug('Logged %s message for %s' %(type_, id_))
                self._qlog_dict[(type_, id_)][0].task_done()
            self._log.debug('Finished Dumping %s - %s Queue' %(type_, id_))
        else:
            while not self._qlog_dict[(type_, id_)][0].empty():
                msg = self._qlog_dict[(type_, id_)][0].get()
                seqNum = msg[0]
                if seqNum > self.last_seqNum:
                    if self.logging:
                        self._qlog_dict[(type_, id_)][1].market(msg[1])
                        self._qlog_dict[(type_, id_)][1].debug('Logged %s message for %s - %s' %(type_, id_, msg[0]))
                self._qlog_dict[(type_, id_)][0].task_done()
            self.last_seqNum = seqNum
            self._log.debug('Finished Dumping %s - %s Queue' %(type_, id_))


    def log(self, msg):
        qlog = self._qlog_dict[(msg['type'], msg['product_id'])]
        try:
            qlog[0].put((msg['sequence'], msg))
        except KeyError as e:
            #self._log.warn('Caught Key Error::Message type \'%s\' has no key \'sequence\'.' % msg['type'])
            qlog[0].put(msg)
        if qlog[0].qsize() > 10:
            self._handleq(msg['type'], msg['product_id'])

