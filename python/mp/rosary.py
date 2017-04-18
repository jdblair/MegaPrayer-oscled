#!/usr/bin/python3
import code
import copy
import threading
import time
import math

from mp import color
from .effects import *
from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

class Bead:
    """Bead represents a single rosary bead."""
    def __init__(self, index=0):
        self.index = index
        self.color = color.Color()
        
    def __repr__(self):
        return "Bead(index={}, color={})".format(self.index, self.color)

    def copy_color(self, color):
        """Helper function that sets the Bead color by copying a Color object."""
        self.color = copy.copy(color)


class Rosary:
    """Rosary represents the whole rosary and the set of effects currently
    running.  It is in charge of animating the rosary by calling
    next() in each running active Effect and transmitting the OSC
    commands set the colors of beads.

    """
    def __init__(self, ip="127.0.0.1", port=5005):
        self.beads = []
        self.bgcolor = color.Color(0,0,0)
        self.effects = []
        self.osc_ip = ip
        self.osc_port = port
        self.effect_id = 0;
        self.BEAD_COUNT=60
        self.run_mainloop = False
        self.mainloop_delay = 0.03
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
        self.Color_White = color.Color(1,1,1)
        self.Color_Red = color.Color(1,0,0)
        self.Color_Yellow = color.Color(1,1,0)
        self.Color_Green = color.Color(0,1,0)
        self.Color_Blue = color.Color(0,0,1)
        self.Color_Violet = color.Color(1,0,1)
        self.Color_Cyan = color.Color(0,1,1)
        self.Color_Black = color.Color(0,0,0)

    def register_effect(self, effect):
        """Register the name of an effect in our effect registry.  This allows
        us to access the effect without having access to the python
        object name itself.

        """
        # instantiate the object so we get get the name
        e = effect(self.Set_None)
        self.effect_registry[e.name] = effect
        
    def add_effect_object(self, effect):
        """Adds an Effect object to the active Effect list.  Returns the id of
        the active effect.

        """
        self.effect_id = self.effect_id + 1
        effect.id = self.effect_id
        effect.rosary = self
        self.effects.append(effect)
        return self.effect_id

    def add_effect(self, name, bead_set, color=color.Color(1,1,1)):
        """Adds an Effect to the active Effect list by using the Effect
        name. Returns the id of the active effect.

        """
        return self.add_effect_object(self.effect_registry[name](bead_set, color))

    def clear_effects(self):
        """Remove all active effects. This stops all activity on the rosary."""
        self.effects = []

    def del_effect(self, id):
        """Delete an active effect by id."""
        self.effects.remove(self.effect(id))

    def effect(self, id):
        """Return the Effect object of an active effect by specifying the Effect id."""
        for e in self.effects:
            if e.id == id:
                return e
        return 0

    def update(self):
        """Transmit the OSC message to update all beads on the rosary."""
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
            
        msg = osc_message_builder.OscMessageBuilder(address = "/update")
        msg = msg.build()
        bundle.add_content(msg)
            
        bundle = bundle.build()
        self.osc_client.send(bundle)

    def mainloop(self):
        """This is the animiation loop. It cycles through all active effects
        and invokes next() on each effect.

        knobs:
        * mainloop_delay: how long to wait, in seconds, at the bottom of each loop

        """
        while (self.run_mainloop):
            for effect in self.effects:
                #print("effect: {}".format(effect.name))
                effect.next(self)
                if (effect.finished):
                    self.del_effect(effect.id)
                self.update()
            time.sleep(self.mainloop_delay)

    def start(self):
        """Start the animation loop (aka, mainloop()) and create a shell for live interaction."""
        r = self
        if (r.run_mainloop == False):
            r.run_mainloop = True
            self.t_mainloop = threading.Thread(name='rosary_mainloop', target=self.mainloop)
            self.t_mainloop.start()

            code.interact(local=locals())

            self.t_mainloop.join()

    def stop(self):
        """Stop the mainloop and exit the application."""
        self.run_mainloop = False
        exit(0)

    def pause(self):
        """Stop the animation loop without exiting."""
        if (self.run_mainloop):
            self.run_mainloop = False

