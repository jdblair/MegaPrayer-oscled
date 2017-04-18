#!/usr/bin/python3
import argparse
from mp import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="OSC server address")
    parser.add_argument("--port", default=5005, help="OSC server port")
    args = parser.parse_args()

    r = rosary.Rosary(args.ip, args.port)

    # create a bounce effect on all beads
    r.add_effect('bounce', r.set_registry['All'])

    # change color to red
    r.effect(1).color.set(r.color_registry['Red'])

    # add another throb on the odd beads
    r.add_effect('throb', r.set_registry['Odd_Ring'], color=r.color_registry['Blue'])

    # add bounce
    r.add_effect('bounce', r.set_registry['All'], color=r.color_registry['Green'])


    r.start()
    

    
