#!/usr/bin/python3
"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

#from . import rosary
from mp import rosary
#import rosary

def print_volume_handler(unused_addr, args, volume):
    print("UNUSED ADDR: {}".format(unused_addr))
    print("ARGS: {}".format(args))
    print("VOLUME: {}".format(volume))
    print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError: pass

r = None
d = None

def add_effect_wrapper(unused_addr, args, effect_name):
    print(args)
    r.add_effect(effect_name, r.set_registry['All'])

def get_effects_wrapper(unused_addr):
    print(args)
    r.get_running_effects()

def trigger_some_shit(unused_addr):
    print(unused_addr)

def set_sleep_wrapper(unused_addr, sleep_sec):
    print("NEW SLEEP: {}".format(sleep_sec))
    r.mainloop_delay = sleep_sec

def clear_effects_wrapper(unused_addr):
    r.clear_effects()


class Test:
    def foo(self, unused_addr, args, stuff):
        print("Hello, {}".format(stuff))


if __name__ == "__main__":

    global r

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    t = Test()

    d = dispatcher.Dispatcher()
    d.map('/test', t.foo)
    d.map("/filter", print)
    d.map("/volume", print_volume_handler, "Volume")
    d.map("/logvolume", print_compute_handler, "Log volume", math.log)
    #dispatcher.map("/add_effect", r.add_effect, 'bounce', r.set_registry['All'])

    d.map("/set_sleep", set_sleep_wrapper)

    d.map("/add_effect", add_effect_wrapper, "name", "bead_set")

    #d.map("/effects", r.get_running_effects)
    d.map("/effects", get_effects_wrapper)

    d.map('/clear_effects', clear_effects_wrapper)

    # TODO: /trigger/<name> to trigger object
    # Examples:
    #   /trigger/rosary/5 i 1
    #   /trigger/rosary/5 i 0
    #   /trigger/nail/left i 1
    d.map("/trigger", trigger_some_shit)

    # ROSARY STUFF
    #r = rosary.Rosary(args.ip, args.port)
    r = rosary.Rosary(args.ip, 5005, d)
    r.start(interactive=False)

    # CLEAN THIS UP
    #r.dispatcher = d

    # TODO: /effect/<id> directly affect a running effect

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), d)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

    print("OH NO")
    # If we exit the server, then have the rosary exit too
    # Err...no worky?
    r.t_mainloop.join()
