import os, sys, threading

sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + '/scripts')
import ticketing

def beginTimed():

    threading.Timer(3, every3seconds).start()

def every3seconds():
    ticketing.updateQty()
    threading.Timer(3, every3seconds).start()