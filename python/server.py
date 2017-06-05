#!/usr/bin/python3
"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

from mp import rosary

def print_dispatcher_paths(unused_addr, d):
    """
    This is so weird. I'm mapping a function to the dispatcher that
    takes an instance of...itself as an argument.
    """

    print("* DISPATCHER PATHS *")
    for k in sorted(d[0]._map.keys()):
        print(k)

def trigger_something(unused_addr):
    print(unused_addr)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--listen-ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--listen-port",
        type=int, default=5006, help="The port to listen on")
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to send messages to")
    parser.add_argument("--port",
        type=int, default=5005, help="The port to send messages to")
    parser.add_argument("--interactive",
        type=bool, default=False, help="start interactive shell");

    args = parser.parse_args()

    d = dispatcher.Dispatcher()
    # Since basically all the paths will be dynamically generated,
    # this will be useful for developing
    # (Especially for checking that paths for cleared effects are removed)
    d.map("/paths", print_dispatcher_paths, d)

    # TODO: /trigger/<name> to trigger object
    # Examples:
    #   /trigger/rosary/5 i 1
    #   /trigger/rosary/5 i 0
    #   /trigger/nail/left i 1
    d.map("/trigger", trigger_something)

    # Since the Rosary itself won't be instantiated often, I don't feel
    # bad about requiring that the dispatcher be passed
    r = rosary.Rosary(args.ip, args.port, d)
    r.start(interactive=args.interactive)

    server = osc_server.ThreadingOSCUDPServer(
        (args.listen_ip, args.listen_port), d)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
