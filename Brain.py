'''
Class that will wrap a tensorflow object -- The "Brain" of the program
Program will continuously be fed new data to analyze.
**SHOULD ONLY START MAKING TRADES WHEN IT FEELS COMFORTABLE DOING SO**
**DO NOT FORCE THE BOT TO TRADE WHEN IT DOESN'T WANT TO**
**BOTS HAVE FEELINGS TOO**

Pub/Sub endpoints are for inter program communications??
    -The brain will request to place a buy/sell order
    -The "conscience" will have the final say on whether the order should be placed
        -Conscience is in charge of determining the limit price
        -Responds to brain with whether the buy/sell is a good idea
        -Like a sanity check; ensures the brain doesn't get any wild ideas
'''
import tensorflow as tf

class Brain:
    def __intit__(self, pub_endpoint, sub_endpoint):
    
    def parseMsg(self, msg):
        #parse and decide if this data has something we can learn from
    
    def teach(self, data):
    
    def request(self, opt = BUY || SELL)
