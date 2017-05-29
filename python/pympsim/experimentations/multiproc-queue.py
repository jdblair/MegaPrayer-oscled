# -*- coding: utf-8 -*-
"""
Created on Sat May  6 19:24:03 2017

@author: 
    http://stackoverflow.com/questions/11515944/how-to-use-multiprocessing-que
    ue-in-python/11516406#11516406
"""

from multiprocessing import Process, Queue
import time

def reader(queue):
    ## Read from the queue
    while True:
        msg = queue.get()         # Read from the queue and do nothing
        if (msg == 'DONE'):
            print("DONESKI")
            break

def writer(count, queue):
    ## Write to the queue
    for ii in range(0, count):
        queue.put(ii)             # Write 'count' numbers into the queue
    queue.put('DONE')

if __name__=='__main__':
    for count in [10**4, 10**5, 10**6]:
        queue = Queue()   # reader() reads from queue
                          # writer() writes to queue
        reader_p = Process(target=reader, args=((queue),))
        reader_p.daemon = True
        reader_p.start()        # Launch reader() as a separate python process

        _start = time.time()
        writer(count, queue)    # Send a lot of stuff to reader()
        reader_p.join()         # Wait for the reader to finish
        print("Sending %s numbers to Queue() took %s seconds" % (count, 
            (time.time() - _start)))
        
        
#Multiprocessing has a feature for Event
#and for  conditions
#and a queue
''' I need to run the GUI and the Server at the same time. The GUI
needs to receive updates telling it what color each bead should be 
at every frame. 

The server is receiving frames plus periodic /update commands.

when the server receives a bead data, it should place it in the queue.
when the server receives an update command, it should set the update 
event to true

when the GUI sees that the update event is true, it should read
all the bead data in the queue and update its own beads.'''