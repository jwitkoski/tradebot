#!/usr/bin/env python
'''
GDAX Web socket for live feed:
wss://ws-feed.gdax.com

There appears to be a python Websocket-client; we'll
use that to sub to the feed above^

Python also has a JSON encoder and decoder that we will use to pack/parse messages
'''

import websocket as ws
import json
from threading import Thread
import types
from time import sleep
from Queue import Queue
        
class DataFeed:

    def __init__(self, addr, pairs, channels):
        self.addr = addr
        self.pairs = pairs
        self.channels = channels
        self.endpoint = ws.create_connection(str(addr))
        self.__msgQ = Queue()
        self.__handleThread = Thread(\
            target = self.__handle_q,\
            name = 'Message_Handler_Thread')
        self.__handleThread.daemon = True
        self.__listenThread = Thread(\
            target = self.__subscribe_and_listen,\
            name = 'Listener_Thread')
        self.__listenThread.daemon = True
        self.__isRunning = False
        self.pendingException = None
        self.__listenThread.start()

    class BaseError(Exception):
        def __init__(self, outer_obj, msg):
            self.outer_obj = outer_obj
            self.err = msg
        def what(self):
            pass 
    
    class SubscribeError(BaseError):
        #Exception raised due to subscribe errors
        def __init__(self, outer_obj, msg):
            super(DataFeed.SubscribeError, self).__init__(outer_obj, msg)
            getattr(self.outer_obj, 'raise_exc')(self)
        def what(self):
            print('DataFeed.SubscribeError: Could not subscribe to desired pair(s)/channel(s) - %s' % self.err)

    def check(self):
        if self.pendingException is not None:
            raise self.pendingException

    def raise_exc(self, err):
        self.pendingException = err

    def clrExc(self):
        self.pendingException = None

    def close(self):
        self.__isRunning = False
        self.__listenThread.join()
        self.__msgQ.join()
        self.__handleThread.join()

         
    def __subscribe_and_listen(self):
        def all_same_type(typ, iterable):
            return all([isinstance(obj, typ) for obj in iterable])
        #Prepare [pairs] for the sub message
        pair_str = []
        if not isinstance(self.pairs, list):
            if isinstance(self.pairs, tuple):
                pair_str = ['-'.join((p.upper() for p in self.pairs))]
            elif isinstance(self.pairs, str):
                pair_str = [self.pairs.upper()]
            else:
                self.SubscribeError(self, 'Invalid Pair Requested')
                return
        else:
            if all_same_type(tuple, self.pairs):
                for pair in self.pairs:
                    pair_str.append('-'.join([pair[i].upper() for i in range(len(pair))]))
            elif all_same_type(str, self.pairs):
                pair_str = [p.upper() for p in self.pairs]
            else:
                self.SubscribeError(self, 'Invalid \'pairs\' Argument: Valid options:\n' + \
                                     '   \'XXX-XXX\'                 One Pair: String\n' + \
                                     '   (\'XXX\', \'XXX\')          One Pair: Tuple\n' + \
                                     '   [\'XXX-XXX\', ...]          Multiple Pairs: String List\n' + \
                                     '   [(\'XXX\', \'XXX\'), ...]   Multiple Pars: List of One Pair Tuples')
                return
        #Prapare [channels] for the sub message
        channel_str = []
        available_channels = ['heartbeat', 'ticker', 'level2', 'user', 'matches', 'full']
        if isinstance(self.channels, list):
            channel_str = [c for c in self.channels if c in available_channels]
        elif isinstance(self.channels, str):
            channel_str = [self.channels]
        else:
            self.SubscribeError(self, 'Invalid \'channels\' Argument: must be a string or list of strings.')
            return
        self.subbed_pairs = pair_str
        self.subbed_channels = channel_str
        #build subscribe message
        sub_msg = json.dumps(\
        {\
            "type": "subscribe",\
            "product_ids": pair_str,\
            "channels": channel_str
        })
        self.endpoint.send(sub_msg)
        self.__isRunning = True
        self.__handleThread.start()
        self.recvLoop()

    def recvLoop(self):
        while self.__isRunning:
            msg = json.loads(self.endpoint.recv())
            if msg['type'] in self.subbed_channels:
                cb = getattr(self, msg['type']+'_cb')
                self.__msgQ.put((cb, msg))
            else:
                self.__msgQ.put((self.unknownType_cb, msg))
            sleep(0.25)
        return

    def __handle_q(self):
        while self.__isRunning or not self.__msgQ.empty():
            task = self.__msgQ.get()
            task[0](task[1])
            self.__msgQ.task_done()

    def unknownType_cb(self, msg):
        print 'Unknown Message type encountered: %s\n' % msg['type']
        print msg

    def heartbeat_cb(self, msg):
        print 'Received Hearbeat Message #%s for %s' % (msg['sequence'], msg['product_id'])
        del msg

        '''
        - Runs on its own thread
        - Subscribe to desired pairs (ie. ETH/USDT) and channels
            -build JSON message
        --------------EXAMPLE----------------
        {
            "type": "subscribe",
            "product_ids": [
                "ETH-USD",
                "ETH-EUR"
            ],
            "channels": [
                "level2",
                "heartbeat",
                {
                    "name": "ticker",
                    "product_ids": [
                        "ETH-BTC",
                        "ETH-USD"
                    ]
                }
            ]
        }
        ---------------------------------------
        - There are different "channels" (CHAN) to subscribe to
            -We will have a set of "callbacks" so if a message of type == 'heartbeat'
            is received, self.heartbeat_cb(msg) will be executed on a new thread
                #Received message = recvd_msg
                #if 'type' in recvd_msg:
                    #func = getattr(self, recvd_msg['type'] + '_cb')
                    #thread(func, recvd_msg)
            -Callbacks will parse the rest of message and send relevant data off to TensorFlow to get learnt
        '''

pairs = input('Input Pairs to Subscribe to:')
df = DataFeed('wss://ws-feed.gdax.com', pairs, 'heartbeat')
try:
    while True:
        df.check()
        sleep(0.5)
except DataFeed.SubscribeError as e:
    e.what()
    df.clrExc()
    raise e
df.close()
