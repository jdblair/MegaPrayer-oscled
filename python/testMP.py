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
    #r.add_effect(name='throb', color='red', bead_set='rosary')

    # add an effect for the cross
    #r.add_effect(name='soft_edges_glow', color='yellow', bead_set='cross')

    # stigmata FTW
    r.add_effect(name='soft_edges_glow', color='red', bead_set='stigmata_left')
    r.add_effect(name='soft_edges_glow', color='red', bead_set='stigmata_right')
    r.add_effect(name='soft_edges_glow', color='yellow', bead_set='stigmata_crown')
    r.add_effect(name='soft_edges_glow', color='red', bead_set='stigmata_feet')

    # add an effect for the bases
    r.add_effect(name='throb', color='yellow', bead_set='bases')

    r.start()
    

    
