#!/usr/bin/python3
import code
import copy
import threading
import time
import math
import inspect

from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

from mp import color, effects

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
    def __init__(self, ip="127.0.0.1", port=5005, dispatcher=None, name="rosary"):
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
        # Reasonable defaults
        self.name = name
        self.dispatcher = dispatcher

        self.osc_client = udp_client.UDPClient(self.osc_ip, self.osc_port)

        for i in range(self.BEAD_COUNT):
            self.beads.append(Bead(i))

        # some useful predefined sets of beads
        self.set_registry = {
            'None': frozenset(),
            'All': frozenset(self.beads),
            'Stem': frozenset(self.beads[0:4]),
            'Ring': frozenset(self.beads[4:60]),
            'Eighth0': frozenset(self.beads[4:11]),
            'Eighth1': frozenset(self.beads[11:18]),
            'Eighth2': frozenset(self.beads[18:25]),
            'Eighth3': frozenset(self.beads[25:32]),
            'Eighth4': frozenset(self.beads[32:39]),
            'Eighth5': frozenset(self.beads[39:46]),
            'Eighth6': frozenset(self.beads[46:53]),
            'Eighth7': frozenset(self.beads[53:60]),
            'Quadrent0': frozenset(self.beads[4:18]),
            'Quadrent1': frozenset(self.beads[18:32]),
            'Quadrent2': frozenset(self.beads[32:46]),
            'Quadrent3': frozenset(self.beads[46:60]),
            'Even_All': frozenset(self.beads[0:60:2]),
            'Even_Ring': frozenset(self.beads[4:60:2]),
            'Odd_All': frozenset(self.beads[1:60:2]),
            'Odd_Ring': frozenset(self.beads[5:60:2])
        }
        self.set_registry['Half01'] = self.set_registry['Quadrent0'].\
                                           union(self.set_registry['Quadrent1'])
        self.set_registry['Half12'] = self.set_registry['Quadrent1'].\
                                           union(self.set_registry['Quadrent2'])
        self.set_registry['Half23'] = self.set_registry['Quadrent2'].\
                                           union(self.set_registry['Quadrent3'])
        self.set_registry['Half30'] = self.set_registry['Quadrent3'].\
                                           union(self.set_registry['Quadrent0'])

        # some useful predefined colors
        self.color_registry = {
            'White': color.Color(1,1,1),
            'Red': color.Color(1,0,0),
            'Yellow': color.Color(1,1,0),
            'Green': color.Color(0,1,0),
            'Blue': color.Color(0,0,1),
            'Violet': color.Color(1,0,1),
            'Cyan': color.Color(0,1,1),
            'Black': color.Color(0,0,0)
        }

        # Automagically register effects
        self.register_defined_effects()

    def register_effect(self, effect):
        """Register the name of an effect in our effect registry.  This allows
        us to access the effect without having access to the python
        object name itself.

        """
        # instantiate the object so we get get the name
        e = effect(self.set_registry['None'])
        self.effect_registry[e.name] = effect

    def find_defined_effects(self, module_or_class):

        classes = set()

        # A little imperfect, as we'll first process imports and
        # we end up trying to add mp.effects.effect.Effect many times
        # We're circumventing this by using a set
        # Inspired by:
        #   http://stackoverflow.com/a/408465
        #   http://stackoverflow.com/a/22578562
        for name, obj in inspect.getmembers(module_or_class):
            if inspect.ismodule(obj) and obj.__package__ == 'mp.effects':
                classes = classes.union(self.find_defined_effects(obj))
            elif inspect.isclass(obj):
                classes.add(obj)

        return classes
        
    def register_defined_effects(self):
        defined_effects = self.find_defined_effects(effects)
        for eff in defined_effects:
            # Don't register abstract classes, e.g. effects.effect.Effect
            if not inspect.isabstract(eff) and issubclass(eff, effects.effect.Effect):
                self.register_effect(eff)


    def add_effect_object(self, effect):
        """Adds an Effect object to the active Effect list.  Returns the id of
        the active effect.

        """
        self.effect_id = self.effect_id + 1
        effect.id = self.effect_id
        # Since rosary holds the dispatcher and the effect doesn't
        # know about rosary on init, we can't map to dispatcher yet either
        effect.rosary = self
        self.effects.append(effect)
        return self.effect_id

    def add_effect(self, name, bead_set, color=color.Color(1,1,1)):
        """Adds an Effect to the active Effect list by using the Effect
        name. Returns the id of the active effect.

        """
        print("ADD THIS EFFECT: {}".format(name))
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

    # Helper while developing the OSC server
    def get_running_effects(self):
        """Return all running effects"""
        print(self.effects)
        return self.effects

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

                # I didn't want to pass the dispatcher through to the effect
                # in its initialization because it feels silly to force
                # Effect writers to always take a dispatcher.
                # Since we're attaching the rosary after initialization anyway
                # I'll just hook onto the first iteration of mainloop to
                # register effects "endpoints" with the dispatcher
                if not effect.registered:
                    effect.register_with_dispatcher()

                effect.next(self)
                if (effect.finished):
                    self.del_effect(effect.id)
                self.update()
            time.sleep(self.mainloop_delay)

    def start(self, interactive=True):
        """Start the animation loop (aka, mainloop()) and create a shell for live interaction."""
        r = self
        if (r.run_mainloop == False):
            r.run_mainloop = True
            self.t_mainloop = threading.Thread(name='rosary_mainloop', target=self.mainloop)
            self.t_mainloop.start()

            # Don't join the thread if being called from server
            if interactive:

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

