# -*- coding: utf-8 -*-
"""
instantiate a process object
with a target function and 
arguments and call start() 
"""

import multiprocessing
from multiprocessing import Queue
import simulator
import OSCserver

def sim(queue):
    print("Starting Simulator...")
    simulator.main(queue)

def serve(queue):
    print("Starting OSC Server...")
    OSCserver.main(queue)


if __name__ == '__main__':
    queue = Queue() 
    p = multiprocessing.Process(target=sim, args=((queue),))
    q = multiprocessing.Process(target=serve, args=((queue),))
    p.start()
    q.start()

