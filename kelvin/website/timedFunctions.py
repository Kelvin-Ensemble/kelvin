import os, sys, threading

sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + '/scripts')
import ticketing

def beginTimed():

    threading.Timer(3, every5seconds).start()

def every5seconds():
    ticketing.updateQty()
    threading.Timer(5, every5seconds).start()