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

def print_dispatcher_paths(unused_addr, args):
    """
    This is so weird. I'm mapping a function to the dispatcher that
    takes an instance of...itself as an argument.
    """

    print("* DISPATCHER PATHS *")
    for k in sorted(args[0].dispatcher._map.keys()):
        print(k)
    print("* ROSARY PATHS *")
    for k in r.dm.exposed_methods.keys():
        print("/rosary/{}".format(k))
    print("* TRIGGER PATHS *")
    for k in r.trigger_registry.keys():
        print("/trigger/{}".format(k))
    print("* EFFECT KNOB PATHS *")
    for k in r.knobs.keys():
        print("/effect/{}".format(k))


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
    args = parser.parse_args()

    d = dispatcher.Dispatcher()
    # Since the Rosary itself won't be instantiated often, I don't feel
    # bad about requiring that the dispatcher be passed
    r = rosary.Rosary(args.ip, args.port, d)

    # Since basically all the paths will be dynamically generated,
    # this will be useful for developing
    # (Especially for checking that paths for cleared effects are removed)
    d.map("/paths", print_dispatcher_paths, r)

    # Since the Rosary itself won't be instantiated often, I don't feel
    # bad about requiring that the dispatcher be passed
    r = rosary.Rosary(args.ip, args.port, d)
    r.start(interactive=False)

    server = osc_server.ThreadingOSCUDPServer(
        (args.listen_ip, args.listen_port), d)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
