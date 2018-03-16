from DataFeed import DataFeed
from logging import getLogger
import httplib as http
from config import settings

#This class will wrap the DataFeed and also be responsible for
#sending the buy/sell orders
#Should also be able to queue orders (without actually placing them)
#So a theoretical infinite amount of orders can be placed
#   ie. Buy one XXX @ $5.00, Sell one XXX @ $7.00, rinse and repeat
class GdaxClient:
    def __init__(self):
        self.log = getLogger('GDAX_Client')
        self.socket_feed = DataFeed(settings['DataFeed'], True)
        if self.startDataFeed():
            self.log.info('Initialized GdaxClient!')

        
    def startDataFeed(self):
        try:
            if self.socket_feed.subscribe():
                self.socket_feed.start()
            else:
                self.log.error('Could not subscribe to all desired channels and pairs!')
                raise Exception('Failed to Subscribe!')
        except DataFeed.SubscribeError as e:
            self.log.error('Caught SubscribeError from DataFeed!')
            self.log.error(e)
            return False
        return True

