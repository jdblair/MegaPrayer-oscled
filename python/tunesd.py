#!/usr/bin/python3

# OSC driven music server for MegaPrayer, part of Burning Man 2017

import argparse
import math
import os
import pygame
import random

from pythonosc import dispatcher
from pythonosc import osc_server

max_channels = 6
pygame.mixer.init(channels=max_channels)

class MegaTunes():
    """The sound server for the 2017 Burning Man project MegaPrayer"""

    def __init__(self):
        self.sound_files_root_dir = "../soundfiles/"
        self.default_sound_file = "default.wav"
        self.id_to_sound_file = {}
        self.active_channel = -1

    def rev_channel(self):
        self.active_channel = self.active_channel + 1
        if self.active_channel >= max_channels:
            self.active_channel = 0

    def block_until_quiet(self):
        """aka pray for silence"""
        print("Blocking until all tracks are done")
        for chan in range(0, max_channels):
            while pygame.mixer.Channel(chan).get_busy() == True:
                continue

    def load_map(self, map_file="../conf/osc_to_musicfile_map.conf"):
        with open(map_file) as f:
            for line in f:
                (id_key, sound_file) = line.split()
                self.id_to_sound_file[int(id_key)] = sound_file

    def osc_print_volume_handler(self, unused_addr, args, volume):
        print("[{0}] ~ {1}".format(args[0], volume))

    def osc_print_compute_handler(self, unused_addr, args, volume):
        try:
            print("[{0}] ~ {1}".format(args[0], args[1](volume)))
        except ValueError:
            pass

    def osc_print_filter_handler(self, thing=""):
        print(thing)

    def osc_play_random(self):
        sound_file = random.choice(os.listdir(self.sound_files_root_dir))
        print("Selecting random sound file: {}".format(sound_file))
        self.play_sound_file(sound_file)

    def osc_play_by_name(self, sound_file=""):
        self.play_sound_file(sound_file)

    def osc_play_by_id(self, unused_addr, args):
        sound_file = self.default_sound_file
        try:
            sound_file = self.id_to_sound_file[args[0]]
        except NameError:
            # play default track vs erroring out?
            print("Could not find sound file for id: {}".format(args[0]))
        self.play_sound_file(sound_file)

    def play_sound_file(self, sound_file=""):
        if sound_file == "":
            sound_file = self.default_sound_file

        self.rev_channel()

        print("Playing sound file: {} on channel: {}".format(sound_file, self.active_channel))

        if self.sound_files_root_dir not in sound_file:
            sound_file = self.sound_files_root_dir + sound_file

        # pygame player
        pygame.mixer.Channel(self.active_channel).play(pygame.mixer.Sound(sound_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen-ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--listen-port",
        type=int, default=5007, help="The port to listen on")
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to send messages to")

    args = parser.parse_args()

    mt = MegaTunes()
    mt.osc_play_by_name()
    mt.block_until_quiet()
    mt.osc_play_random()
    mt.osc_play_random()
    mt.osc_play_random()
    mt.osc_play_random()
    mt.osc_play_random()
    mt.osc_play_random()
    mt.osc_play_random()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", mt.osc_print_filter_handler, "Filter")
    dispatcher.map("/volume", mt.osc_print_volume_handler, "Volume")
    dispatcher.map("/logvolume", mt.osc_print_compute_handler, "Log volume", math.log)

    # MegaPrayer actions
    dispatcher.map("/audio/play/id", mt.osc_play_by_id, "Play by ID")
    dispatcher.map("/audio/play/name", mt.osc_play_by_name, "Play by Name")
    dispatcher.map("/audio/play/random", mt.osc_play_by_name, "Play Rando")

    server = osc_server.ThreadingOSCUDPServer(
        (args.listen_ip, args.listen_port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

    pass


