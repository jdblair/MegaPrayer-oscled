#!/usr/bin/python3

import argparse
import random
import time
import math
import threading
import code

from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder
from pythonosc import udp_client


class Color:
    """Data structure for holding individual Bead color data"""
    
    def __init__(self, r=0, g=0, b=0, a=0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
         return "Color({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)

    def set(self, color):
        self.r = color.r
        self.g = color.g
        self.b = color.b
        self.a = color.a

    def set(self, color, intensity=1):
        self.r = color.r * intensity
        self.g = color.g * intensity
        self.b = color.b * intensity
        self.a = color.a


class Bead:
    def __init__(self, index=0):
        self.index = index
        self.color = Color()
        
    def __repr__(self):
        return "Bead(index={}, color={})".format(self.index, self.color)

class Rosary:
    def __init__(self):
        self.beads = []
        self.bgcolor = Color(0,0,0)
        self.effects = []
        self.osc_ip = "127.0.0.1"
        self.osc_port = 5005
        self.effect_id = 0;
        self.BEAD_COUNT=60
        self.run_mainloop = False
        self.mainloop_sleep = 0.1
        self.effect_registry = {}

        self.osc_client = udp_client.UDPClient(self.osc_ip, self.osc_port)

        for i in range(self.BEAD_COUNT):
            self.beads.append(Bead(i))

        # some useful predefined sets of beads
        self.Set_All = frozenset(self.beads)
        self.Set_Stem = frozenset(self.beads[0:4])
        self.Set_Ring = frozenset(self.beads[4:60])
        self.Set_Half01 = frozenset(self.beads[4:32])
        self.Set_Half12 = frozenset(self.beads[18:46])
        self.Set_Half23 = frozenset(self.beads[32:60])
        self.Set_Half30 = frozenset(self.beads[46:4])
        self.Set_Quadrent0 = frozenset(self.beads[4:18])
        self.Set_Quadrent1 = frozenset(self.beads[18:32])
        self.Set_Quadrent2 = frozenset(self.beads[32:46])
        self.Set_Quadrent3 = frozenset(self.beads[46:60])
        self.Set_Even_All = frozenset(self.beads[0:60:2])
        self.Set_Even_Ring = frozenset(self.beads[4:60:2])
        self.Set_Odd_All = frozenset(self.beads[1:60:2])
        self.Set_Odd_Ring = frozenset(self.beads[5:60:2])

        # some useful predefined colors
        self.Color_White = Color(1,1,1)
        self.Color_Red = Color(1,0,0)
        self.Color_Yellow = Color(1,1,0)
        self.Color_Green = Color(0,1,0)
        self.Color_Blue = Color(0,0,1)
        self.Color_Violet = Color(1,0,1)
        self.Color_Cyan = Color(0,1,1)
        
    def add_effect(self, effect):
        self.effects.append(effect)
        self.effect_id = self.effect_id + 1
        effect.id = self.effect_id
        effect.rosary = self
        return self.effect_id

    def clear_effects(self):
        self.effects = []

    def update(self):
        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)

        i = 0
        while (i < self.BEAD_COUNT):
            #print("bead {}".format(i))
            msg = osc_message_builder.OscMessageBuilder(address = "/beadf")
            msg.add_arg(i)
            msg.add_arg(float(self.beads[i].color.r))
            msg.add_arg(float(self.beads[i].color.g))
            msg.add_arg(float(self.beads[i].color.b))
            msg = msg.build()
            bundle.add_content(msg)
            i = i + 1
        
        bundle = bundle.build()
        self.osc_client.send(bundle)

    def mainloop(self):
        while (self.run_mainloop):
            for effect in self.effects:
                #print("effect: {}".format(effect.name))
                effect.next(self)
                self.update()
            time.sleep(self.mainloop_sleep)

    def start(self):
        r = self
        if (r.run_mainloop == False):
            r.run_mainloop = True
            self.t_mainloop = threading.Thread(name='rosary_mainloop', target=self.mainloop)
            self.t_mainloop.start()
            code.interact(local=locals())
            self.t_mainloop.join()

    def stop(self):
        self.run_mainloop = False
        exit(0)

    def pause(self):
        if (self.run_mainloop):
            self.run_mainloop = False


class Effect:

    """convenience function for converting sets to lists"""
    def bead_set_to_list(self, set):
        beads = []
        for bead in set:
            beads.append(bead)
        beads.sort(key=lambda bead: bead.index)
        return beads
            
class Effect_Snake(Effect):

    def __init__(self, color, length=1, direction=1):
        self.name = "snake"
        self.front = 4
        self.rear = 4
        self.color = color
        self.length = length
        self.direction = direction

    def next(self, rosary):
        rosary.beads[self.rear] = rosary.bgcolor

        if (self.direction > 0):
            self.front = self.front + 1
            if (((self.rear - 4 + self.length) % 56) + 4 < self.front):
                self.rear = self.rear + 1
        else:
            self.front = self.front - 1
            if (((self.rear - 4 - self.length) % 56) + 4 > self.front):
                self.rear = self.rear - 1

        self.front = ((self.front - 4) % 56) + 4
        self.rear = ((self.rear - 4) % 56) + 4

        rosary.beads[self.front] = self.color


class Effect_SineWave(Effect):

    def __init__(self, bead_set, color=Color(1,1,1), period=1, direction=1):
        self.name = "sine_wave"
        self.color = color
        self.offset = 0
        self.period = period
        self.direction = direction
        self.bead_list = self.bead_set_to_list(bead_set)  # cache the ordered list

    def next(self, rosary):
        for b in (self.bead_list):
            intensity = (math.sin((2 * math.pi / len(self.bead_list) * self.period) * (b.index + self.offset)) + 1) / 2
            b.color.set(self.color, intensity)            
        self.offset = (self.offset) + self.direction % 56
            

    
if __name__ == "__main__":
    r = Rosary()
    # r.add_effect(Effect_Snake(Color(0, 1, 0), length=2, direction=-1))
    # r.add_effect(Effect_Snake(Color(0, 1, 1), length=3))
    #r.add_effect(Effect_SineWave(Color(0, 0, 1), period=3, direction=1))
    r.add_effect(Effect_SineWave(r.Set_Half01, color=Color(1, 1, 0), period=2, direction=-1))
    r.add_effect(Effect_SineWave(r.Set_Half23, color=Color(0, 0, 1), period=2, direction=1))

    r.start()
