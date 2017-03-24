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
    def __init__(self, ip="127.0.0.1", port=5005):
        self.beads = []
        self.bgcolor = Color(0,0,0)
        self.effects = []
        self.osc_ip = ip
        self.osc_port = port
        self.effect_id = 0;
        self.BEAD_COUNT=60
        self.run_mainloop = False
        self.mainloop_sleep = 0.1
        self.effect_registry = {}

        self.osc_client = udp_client.UDPClient(self.osc_ip, self.osc_port)

        for i in range(self.BEAD_COUNT):
            self.beads.append(Bead(i))

        # some useful predefined sets of beads
        
        self.Set_None = frozenset()
        self.Set_All = frozenset(self.beads)
        self.Set_Stem = frozenset(self.beads[0:4])
        self.Set_Ring = frozenset(self.beads[4:60])
        self.Set_Eighth0 = frozenset(self.beads[4:11])
        self.Set_Eighth1 = frozenset(self.beads[11:18])
        self.Set_Eighth2 = frozenset(self.beads[18:25])
        self.Set_Eighth3 = frozenset(self.beads[25:32])
        self.Set_Eighth4 = frozenset(self.beads[32:39])
        self.Set_Eighth5 = frozenset(self.beads[39:46])
        self.Set_Eighth6 = frozenset(self.beads[46:53])
        self.Set_Eighth7 = frozenset(self.beads[53:60])
        self.Set_Quadrent0 = frozenset(self.beads[4:18])
        self.Set_Quadrent1 = frozenset(self.beads[18:32])
        self.Set_Quadrent2 = frozenset(self.beads[32:46])
        self.Set_Quadrent3 = frozenset(self.beads[46:60])
        self.Set_Half01 = frozenset(self.Set_Quadrent0.union(self.Set_Quadrent1))
        self.Set_Half12 = frozenset(self.Set_Quadrent1.union(self.Set_Quadrent2))
        self.Set_Half23 = frozenset(self.Set_Quadrent2.union(self.Set_Quadrent3))
        self.Set_Half30 = frozenset(self.Set_Quadrent3.union(self.Set_Quadrent0))
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

    def register_effect(self, effect):
        # instantiate the object so we get get the name
        e = effect(self.Set_None)
        self.effect_registry[e.name] = effect
        
    def add_effect(self, effect):
        self.effect_id = self.effect_id + 1
        effect.id = self.effect_id
        effect.rosary = self
        self.effects.append(effect)
        return self.effect_id

    def add_effect_by_name(self, name, bead_set, color=Color(1,1,1)):
        return self.add_effect(self.effect_registry[name](bead_set, color))

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
    def __init__(self, name, set, color=Color(1,1,1)):
        self.name = name
        self.bead_set = self.set_bead_set(set)
        self.color = Color()
        self.color.set(color)
        self.duration = 0

    """convenience function for converting sets to lists"""
    def set_bead_set(self, set):
        beads = []
        for bead in set:
            beads.append(bead)
        beads.sort(key=lambda bead: bead.index)
        self.bead_list = beads

    def get_name(self):
        return self.name

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
        super().__init__("sine_wave", bead_set, color=color)
        self.offset = 0
        self.period = period
        self.direction = direction

    def next(self, rosary):
        for b in (self.bead_list):
            intensity = (math.sin((2 * math.pi / len(self.bead_list) * self.period) * (b.index + self.offset)) + 1) / 2
            b.color.set(self.color, intensity)            
        self.offset = (self.offset) + self.direction % 56
            

class Effect_ThreePhaseSineWave(Effect):

    def __init__(self, bead_set, color=Color(1,1,1), period=1, direction=1):
        super().__init__("3phase_sine_wave", bead_set, color=color)
        self.offset = 0
        self.period = period
        self.direction = direction
        self.phase_r = 0
        self.phase_g = .25
        self.phase_b = .5

    def next(self, rosary):
        bead_count = len(self.bead_list)
        phase_r = self.phase_r * bead_count
        phase_g = self.phase_g * bead_count
        phase_b = self.phase_b * bead_count

        for bead in (self.bead_list):
            bead.color.r = ((math.sin((2 * math.pi / bead_count * self.period) * (bead.index + self.offset + phase_r)) + 1) / 2) * self.color.r
            bead.color.g = ((math.sin((2 * math.pi / bead_count * self.period) * (bead.index + self.offset + phase_g)) + 1) / 2) * self.color.g
            bead.color.b = ((math.sin((2 * math.pi / bead_count * self.period) * (bead.index + self.offset + phase_b)) + 1) / 2) * self.color.b
        self.offset = (self.offset) + self.direction % bead_count


class Effect_SetColor(Effect):
    def __init__(self, bead_set, color=Color()):
        super().__init__("set_color", bead_set, color=color)

    def next(self, rosary):
        for bead in (self.bead_list):
            bead.color.set(self.color)

class Effect_Bounce(Effect):
    def __init__(self, bead_set, color=Color(), direction=1):
        super().__init__("bounce", bead_set, color=color)
        self.direction = direction
        if (self.direction < 0):
            self.current = len(self.bead_list) - 1
        else:
            self.current = 0
        self.last = self.current

    def next(self, rosary):
        self.bead_list[self.last].color.set(rosary.bgcolor)
        self.current += self.direction
        self.last = self.current
        self.bead_list[self.current].color.set(self.color)
        if (self.current >= (len(self.bead_list) - 1) or self.current <= 0):
            self.direction *= -1


class Effect_Throb(Effect):
    def __init__(self, bead_set, color=Color()):
        super().__init__("throb", bead_set, color=color)
        self.x = 0.0

    def next(self, rosary):
        intensity = (math.sin(self.x * math.pi) + 1) / 2
        for bead in (self.bead_list):
            bead.color.set(self.color, intensity=intensity)
        self.x += 0.05
    
if __name__ == "__main__":
    r = Rosary("192.168.100.114", 5005)

    r.register_effect(Effect_SineWave)
    r.register_effect(Effect_ThreePhaseSineWave)
    r.register_effect(Effect_SetColor)
    r.register_effect(Effect_Throb)
    r.register_effect(Effect_Bounce)

    # r.add_effect(Effect_Snake(Color(0, 1, 0), length=2, direction=-1))
    # r.add_effect(Effect_Snake(Color(0, 1, 1), length=3))
    #r.add_effect(Effect_SineWave(Color(0, 0, 1), period=3, direction=1))
    #r.add_effect(Effect_SineWave(r.Set_Half01, color=Color(1, 1, 0), period=2, direction=-1))
    #r.add_effect(Effect_SineWave(r.Set_Half23, color=Color(0, 1, 1), period=2, direction=1))

#    r.add_effect(Effect_Bounce(r.Set_Ring, color=r.Color_Violet))
#    r.add_effect(Effect_Bounce(r.Set_Ring, color=r.Color_Yellow, direction=-1))
#    r.add_effect(Effect_Bounce(r.Set_Ring, color=r.Color_Violet))
#    r.add_effect(Effect_Bounce(r.Set_Ring, color=r.Color_Violet))

#    r.add_effect(Effect_Bounce(r.Set_Eighth0, color=r.Color_Red))
#    r.add_effect(Effect_Bounce(r.Set_Eighth1, color=r.Color_Red))
#    r.add_effect(Effect_Bounce(r.Set_Eighth2, color=r.Color_Red))
#    r.add_effect(Effect_Bounce(r.Set_Eighth3, color=r.Color_Red))
#    r.add_effect(Effect_Bounce(r.Set_Eighth4, color=r.Color_Blue, direction=-1))
#    r.add_effect(Effect_Bounce(r.Set_Eighth5, color=r.Color_Blue, direction=-1))
#    r.add_effect(Effect_Bounce(r.Set_Eighth6, color=r.Color_Blue, direction=-1))
#    r.add_effect(Effect_Bounce(r.Set_Eighth7, color=r.Color_Blue, direction=-1))

#    r.add_effect(Effect_ThreePhaseSineWave(r.Set_Stem | r.Set_Eighth7 | r.Set_Eighth0, Color(1, 1, 1), period=1, direction=1))
    r.add_effect(Effect_ThreePhaseSineWave(r.Set_Odd_All, Color(1, 1, 1), period=1, direction=1))
    r.add_effect(Effect_ThreePhaseSineWave(r.Set_Even_All, Color(1, 1, 1), period=1, direction=-1))
            
    r.start()
