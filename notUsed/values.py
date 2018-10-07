T = 1
G = 100
D = 1
M = 10
C = 10
i = 0
v = [1,2,3,4]


import threading
import time

def clock(args):
    print(str(args)+" It's "+str(time.ctime()))
    next=int(args[0])+1

    threading.Timer(0.001, clock, [str(next)]).start()

clock(v)
