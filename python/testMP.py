#!/usr/bin/python3
import argparse
from mp import *
from pythonosc import dispatcher

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="OSC server address")
    parser.add_argument("--port", default=5005, help="OSC server port")
    args = parser.parse_args()

    d = dispatcher.Dispatcher()
    r = rosary.Rosary(args.ip, args.port, d)

    # create a bounce effect on all beads
    #r.add_effect('bounce', r.set_registry['All'])
    #r.add_effect('casino', 'all')

    # change color to red
    #r.effect(1).color.set(r.color_registry['red'])

    # add another throb on the odd beads
    r.add_effect(name='throb', color='red', bead_set='all')

    # add an effect for the cross
    r.add_effect(name='throb', color='blue', bead_set='cross')

    # add bounce
    #r.add_effect('casino', 'all', color_name_or_r='green')


    r.start()
    

    
