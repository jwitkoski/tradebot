import DataFeed as Feed
import httplib as http
from config import settings

#This class will wrap the DataFeed and also be responsible for
#sending the buy/sell orders
#Should also be able to queue orders (without actually placing them)
#So a theoretical infinite amount of orders can be placed
#   ie. Buy one XXX @ $5.00, Sell one XXX @ $7.00, rinse and repeat
class GdaxClient:
    def __init__(self):
        self.socket_feed = Feed(settings['DataFeed'], True)
