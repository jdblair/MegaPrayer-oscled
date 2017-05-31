#!/usr/bin/python3
import ast
import code
import copy
import threading
import time
import math
import inspect
import random

from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder

from mp import color, effects, triggers
from mp.dispatcher_mapper import DispatcherMapper

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

    # Can't decorate with @self.r, so need this here
    dm = DispatcherMapper()

    def __init__(self, ip="127.0.0.1", port=5005, dispatcher=None, name="rosary"):
        self.beads = []
        self.bgcolor = color.Color(0,0,0)
        self.effects = []
        self.triggers = {}
        self.osc_ip = ip
        self.osc_port = port
        self.effect_id = 0
        self.trigger_id = 0
        self.BEAD_COUNT=60
        self.run_mainloop = False
        self.mainloop_delay = 0.03
        self.effect_registry = {}
        # Reasonable defaults
        self.name = name
        self.dispatcher = dispatcher
        # This will get populated as effects get deleted
        self.effect_paths_to_unregister = []
        # Available knobs to turn
        self.knobs = {}

        self.osc_client = udp_client.UDPClient(self.osc_ip, self.osc_port)

        for i in range(self.BEAD_COUNT):
            self.beads.append(Bead(i))

        # some useful predefined sets of beads
        self.set_registry = {
            'none': frozenset(),
            'all': frozenset(self.beads),
            'stem': frozenset(self.beads[0:4]),
            'ring': frozenset(self.beads[4:60]),
            'eighth0': frozenset(self.beads[4:11]),
            'eighth1': frozenset(self.beads[11:18]),
            'eighth2': frozenset(self.beads[18:25]),
            'eighth3': frozenset(self.beads[25:32]),
            'eighth4': frozenset(self.beads[32:39]),
            'eighth5': frozenset(self.beads[39:46]),
            'eighth6': frozenset(self.beads[46:53]),
            'eighth7': frozenset(self.beads[53:60]),
            'quadrent0': frozenset(self.beads[4:18]),
            'quadrent1': frozenset(self.beads[18:32]),
            'quadrent2': frozenset(self.beads[32:46]),
            'quadrent3': frozenset(self.beads[46:60]),
            'even_all': frozenset(self.beads[0:60:2]),
            'even_ring': frozenset(self.beads[4:60:2]),
            'odd_all': frozenset(self.beads[1:60:2]),
            'odd_ring': frozenset(self.beads[5:60:2])
        }
        self.set_registry['half01'] = self.set_registry['quadrent0'].\
                                           union(self.set_registry['quadrent1'])
        self.set_registry['half12'] = self.set_registry['quadrent1'].\
                                           union(self.set_registry['quadrent2'])
        self.set_registry['half23'] = self.set_registry['quadrent2'].\
                                           union(self.set_registry['quadrent3'])
        self.set_registry['half30'] = self.set_registry['quadrent3'].\
                                           union(self.set_registry['quadrent0'])

        # some useful predefined colors
        self.color_registry = {
            'white': color.Color(1,1,1),
            'red': color.Color(1,0,0),
            'yellow': color.Color(1,1,0),
            'green': color.Color(0,1,0),
            'blue': color.Color(0,0,1),
            'violet': color.Color(1,0,1),
            'cyan': color.Color(0,1,1),
            # It's annoying when the sim picks black and I can't see anything
            # NOTE YUNFAN: Take this out (maybe) going into prod?
            #'black': color.Color(0,0,0)
        }

        # Automagically register effects so that they're callable by name
        self.register_defined_effects()

        # Map our own exposed methods to the dispatcher
        #self.register_with_dispatcher()
        self.register_with_dispatcher_new()

        # Trigger stuff
        self.register_defined_triggers()


    def register_effect(self, effect):
        """Register the name of an effect in our effect registry.  This allows
        us to access the effect without having access to the python
        object name itself.

        """
        # instantiate the object so we get get the name
        e = effect(self.set_registry['none'])
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


    def register_trigger(self, trigger_class):

        print("REGISTER A TRIGGER")
        print(trigger_class)

        # Instantiate
        self.trigger_id += 1
        trigger = trigger_class()
        trigger.rosary = self
        trigger.id = self.trigger_id
        self.triggers[trigger.name] = trigger

        print("WHAT ARE MY TRIGGERS")
        print(self.triggers)

        self.dispatcher.map(trigger.osc_path,
                            trigger.trigger_wrapper,
                            trigger)


    def find_defined_triggers(self, module_or_class):
        """
        Crawl through mp.triggers package and find (non-abstract) subclasses
        to register with the rosary
        """

        classes = set()
        for name, obj in inspect.getmembers(module_or_class):
            if inspect.ismodule(obj) and obj.__package__ == 'mp.triggers':
                classes = classes.union(self.find_defined_triggers(obj))
            elif inspect.isclass(obj):
                classes.add(obj)

        return classes
        

    def register_defined_triggers(self):
        """
        Figure out which triggers are defined in .py files, and register them
        """

        defined_triggers = self.find_defined_triggers(triggers)
        for tr in defined_triggers:
            # Don't register abstract classes, e.g. effects.effect.Effect
            if not inspect.isabstract(tr) and issubclass(tr, triggers.trigger.Trigger):
                self.register_trigger(tr)


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


    @dm.expose()
    def add_effect(self, *args, **kwargs):
        print("ADD EFFECT NEW")
        print("ARGS: {}".format(args))
        print("KWARGS: {}".format(kwargs))

        effect_name = kwargs.get('name')
        bead_set_name = kwargs.get('bead_set', 'all')
        color_name = kwargs.get('color', 'white')
        r = kwargs.get('r', 0.0)
        g = kwargs.get('g', 0.0)
        b = kwargs.get('b', 0.0)

        # If you don't pass in a good name I'll pretend I didn't hear you
        bead_set = self.set_registry.get(bead_set_name.lower(),
                                         self.set_registry['all'])

        if any([r, g, b]):
            effect_color = color.Color(r, g, b)
        else:
            effect_color = self.color_registry.get(color_name.lower())
        # If all else fails, just pick a random color from the registry
        while effect_color in (None, color.Color(0,0,0)):
            effect_color = random.choice(list(self.color_registry.values()))

        # Whether we're overwriting the string or setting for the first time,
        # it's all the same to us
        kwargs['bead_set'] = bead_set
        kwargs['color'] = effect_color
        print("EFFECT {} USING BEAD SET: {}, COLOR: {}".format(effect_name, bead_set, effect_color))

        # I'd rather be fancy and strip out kwargs that won't be accepted
        # than force people writing effects to take **kwargs /flex
        requested_effect = self.effect_registry.get(effect_name)
        requested_effect_args = inspect.getargspec(requested_effect).args

        # Er, "clean up" the kwargs to pass to an effect init method
        for key in list(kwargs):
            if key not in requested_effect_args:
                kwargs.pop(key)

        if requested_effect is not None:
            return self.add_effect_object(requested_effect(*args, **kwargs))
        else:
            return None


    @dm.expose()
    def clear_effects(self):
        """Remove all active effects. This stops all activity on the rosary."""
        # There's some weird race condition where del_effect's call to
        # self.effects.remove doesn't reorder the list in time if we use
        # a for loop, so do this instead
        while self.effects:
            effect = self.effects[0]
            self.del_effect(effect.id)

        # I know on the real rosary this is unneccessary, but it's
        # annoying on the sim: @jdblair is sending 0,0,0 in the real
        # thing wonky?
        self.add_effect('set_color', 'all', 0, 0, 0)

    @dm.expose()
    def del_effect(self, id):
        """Delete an active effect by id."""

        effect = self.effect(id)

        if effect is not None:
            #effect_paths = [effect.generate_osc_path(fn) for fn in\
            #                effect.dm.registered_methods.keys()]
            #self.effect_paths_to_unregister.extend(effect_paths)
            self.unregister_effect_knobs(effect)
            self.effects.remove(effect)


    def effect(self, id):
        """Return the Effect object of an active effect by specifying the Effect id."""
        for e in self.effects:
            if e.id == id:
                return e
        return None

    # Helper while developing the OSC server
    @dm.expose()
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

        # If we need to unregister effects' paths from the dispatcher,
        # do it here
        while self.effect_paths_to_unregister:
            self.dispatcher._map.pop(self.effect_paths_to_unregister.pop())


    def unregister_effect_knobs(self, effect):
        """
        Given an effect, find all mappings in self.knobs
        involving effect, and remove them
        """

        # NOTE: self.knobs looks like:
        # {
        #   'set_color': [
        #       (<function reference>, <effect instance>),
        #       (<function reference>, <effect instance>)
        #   ]
        # }


        # Use list instead of self.knobs.keys() to avoid
        # "RuntimeError: dictionary changed size during iteration"
        # https://stackoverflow.com/a/11941855
        for fn_name in list(self.knobs):
            mappings = self.knobs[fn_name]
            # Traverse backwards so that we can remove items without
            # accidentally skipping an item due to timing
            for mapping in reversed(mappings):
                mapped_fn = mapping[0]
                mapped_effect = mapping[1]
                if effect == mapped_effect:
                    mappings.remove(mapping)

            # If self.knobs[fn_name] is left with an empty list,
            # remove `fn_name` from self.knobs as well
            if len(mappings) < 1:
                self.knobs.pop(fn_name)

    def register_effect_knobs(self, effect):
        """
        Given an effect, create mappings in self.knobs to effect's
        `dm.expose()`-ed functions
        """

        if not effect.registered:
            for fn_name, fn in effect.dm.registered_methods.items():
                if fn_name in self.knobs.keys():
                    self.knobs[fn_name].append( (fn, effect) )
                else:
                    self.knobs[fn_name] = [ (fn, effect) ]

            effect.registered = True


    def mainloop(self):
        """This is the animiation loop. It cycles through all active effects
        and invokes next() on each effect.

        knobs:
        * mainloop_delay: how long to wait, in seconds, at the bottom of each loop

        """
        while (self.run_mainloop):

            for effect in self.effects:

                # If any new effects have been added since the last iteration,
                # add their knobs to the dispatched functikon
                self.register_effect_knobs(effect)

                effect.next(self)
                if (effect.finished):
                    self.del_effect(effect.id)

            self.update()

            # Let the triggers figure out for themselves what to do
            for trigger in self.triggers.values():
                if trigger.running:
                    trigger.next()

            time.sleep(self.mainloop_delay)

    @dm.expose()
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

    @dm.expose()
    def stop(self):
        """Stop the mainloop and exit the application."""
        self.run_mainloop = False
        exit(0)

    @dm.expose()
    def pause(self):
        """Stop the animation loop without exiting."""
        if (self.run_mainloop):
            self.run_mainloop = False

    def some_shit(self, full_path, *args, **kwargs):
        print("PATH: {}".format(full_path))
        print("ARGS: {}".format(args))
        print("KWARGS: {}".format(kwargs))

        knob_args = full_path.split('/knob/')[-1]
        print("KNOB NAME: {}".format(knob_args))
        parsed_args = knob_args.split('/')
        # We know that the first thing is the knob name
        knob_name = parsed_args.pop(0)
        # Expect there to be an even-numbered count

        print("LEFTOVER ARGS")
        print(args)
        print(len(args))
        print(len(args)/2)

        # IF WE DECIDE TO INFER KWARGS USE THIS
        inferred_kwargs = {}
        for i in range(int(len(parsed_args)/2)):
            implied_arg = parsed_args[i*2]
            implied_val = parsed_args[i*2 + 1]

            # Convert strings representing ints to ints and
            # strings representing floats to floats
            try:
                implied_val = ast.literal_eval(implied_val)
            except ValueError:
                pass

            inferred_kwargs[implied_arg] = implied_val

        print("PASSED ARGS")
        print(args)
        print("I CAN READ!")
        print(inferred_kwargs)

        # If we have inferred kwargs, use them
        # Otherwise, use whatever is in passed args
        # If nothing, assume a 1 from passed args
        if inferred_kwargs:
            self.turn_knob(knob_name, **inferred_kwargs)
        else:
            self.turn_knob(knob_name, *args)

    def other_shit(self, full_path, *args, **kwargs):
        print("PATH: {}".format(full_path))
        print("ARGS: {}".format(args))
        print("KWARGS: {}".format(kwargs))

        knob_args = full_path.split('/rosary/')[-1]
        print("ROSARY FN NAME: {}".format(knob_args))
        parsed_args = knob_args.split('/')
        # We know that the first thing is the knob name
        knob_name = parsed_args.pop(0)
        # Expect there to be an even-numbered count

        print("LEFTOVER ARGS")
        print(args)
        print(len(args))
        print(len(args)/2)

        # IF WE DECIDE TO INFER KWARGS USE THIS
        inferred_kwargs = {}
        for i in range(int(len(parsed_args)/2)):
            implied_arg = parsed_args[i*2]
            implied_val = parsed_args[i*2 + 1]

            # Convert strings representing ints to ints and
            # strings representing floats to floats
            try:
                implied_val = ast.literal_eval(implied_val)
            except ValueError:
                pass

            inferred_kwargs[implied_arg] = implied_val

        print("PASSED ARGS")
        print(args)
        print("I CAN READ!")
        print(inferred_kwargs)

        # If we have inferred kwargs, use them
        # Otherwise, use whatever is in passed args
        # If nothing, assume a 1 from passed args
        if inferred_kwargs:
            #self.turn_knob(knob_name, **inferred_kwargs)
            if knob_name in self.dm.registered_methods.keys():
                self.dm.registered_methods[knob_name](self, **inferred_kwargs)
        else:
            #self.turn_knob(knob_name, *args)
            if knob_name in self.dm.registered_methods.keys():
                self.dm.registered_methods[knob_name](self, *args)


    def register_with_dispatcher_new(self):
        """
        Wildcard handler for knobs
        """

        self.dispatcher.map("/rosary/*", self.other_shit)
        self.dispatcher.map("/knob/*", self.some_shit)


    def turn_knob(self, knob_name, *args, **kwargs):
        """
        
        """

        print("TURN THE KNOB!")
        print("knob_name: {}".format(knob_name))
        print("args: {}".format(args))
        print("kwargs: {}".format(kwargs))

        for fn, instance in self.knobs.get(knob_name, []):
            fn(instance, *args, **kwargs)
