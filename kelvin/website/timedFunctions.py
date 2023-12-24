import threading

import ticketing

def beginTimed():

    threading.Timer(3, every5seconds).start()

def every5seconds():
    ticketing.updateQty()
    threading.Timer(5, every5seconds).start()