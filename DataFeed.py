'''
GDAX Web socket for live feed:
wss://ws-feed.gdax.com

There appears to be a python Websocket-client; we'll
use that to sub to the feed above^

Python also has a JSON encoder and decoder that we will use to pack/parse messages
'''
import websocket as ws
import json
        
class DataFeed:
    def __init__(self, addr, [pairs], [channels]):
        self.addr = addr
        self.endpoint = ws.WebSocket()
        self.endpoint.connect(str(addr),...)
        
    def listen(self):
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
