#!/usr/bin/python3
import ast
import code
import copy
import threading
import time
import math
import inspect
import random
import struct

from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder
from pythonosc import osc_server

from mp import color, effects, triggers
from mp.dispatcher_mapper import DispatcherMapper

class Bead:
    """Bead represents a single rosary bead."""
    def __init__(self, index=0):
        self.index = int(index)
        self.color = color.Color()
        
    def __repr__(self):
        return "Bead(index={}, color={})".format(self.index, self.color)


class Updater:
    def __init__(self, name='', bead_list=[], osc_client=None):
        self.name = name
        self.bead_list = bead_list
        self.osc_client=osc_client
        
    def update(self):
        msg = osc_message_builder.OscMessageBuilder(address = "/bead")
        msg.add_arg(self.name)                 # name (class)
        msg.add_arg(int(0))                    # base
        msg.add_arg(int(len(self.bead_list)))  # length
        
        payload = bytearray()
        for bead in self.bead_list:
            payload.extend(struct.pack('!HHHH',
                                       int(bead.color.r * 0xffff),
                                       int(bead.color.g * 0xffff),
                                       int(bead.color.b * 0xffff),
                                       int(bead.color.brightness)
            ))

        msg.add_arg(bytes(payload))

        self.osc_client.send(msg.build())


class Rosary:
    """Rosary represents the whole rosary and the set of effects currently
    running.  It is in charge of animating the rosary by calling
    next() in each running active Effect and transmitting the OSC
    commands set the colors of beads.
    """

    # Can't decorate with @self.r, so need this here
    dm = DispatcherMapper()

    def __init__(self,
                 ip="127.0.0.1",
                 port=5005,
                 dispatcher=None,
                 name="rosary",
                 server_ip="127.0.0.1",
                 server_port=5006):
        self.beads = []
        self.bases = []
        self.cross = []
        self.triggers = []
        self.bgcolor = color.Color(0,0,0,1)  # note opaque alpha channel
        self.osc_ip = ip
        self.osc_port = port
        self.trigger_id = 0
        self.BEAD_COUNT=60
        self.BASE_COUNT=9
        self.CROSS_LED_COUNT=480
        self.run_mainloop = False
        self.frame_time = 1 / 30   # reciprocal of fps
        self.effect_registry = {}
        self.trigger_registry = {}
        # Allow effects to take over triggers
        self.trigger_hijacks = {}
        # Reasonable defaults
        self.name = name
        self.dispatcher = dispatcher
        # Available knobs to turn
        self.knobs = {}
        self.updater_list = []

        self.osc_server_ip=server_ip
        self.osc_server_port=server_port

        self.osc_client = udp_client.UDPClient(self.osc_ip, self.osc_port)

        # create the three classes of LED "beads"
        for i in range(self.BEAD_COUNT):
            self.beads.append(Bead(i))
        self.updater_list.append(Updater(name='rosary',
                                         bead_list=self.beads,
                                         osc_client=self.osc_client))

        for i in range(self.BASE_COUNT):
            self.bases.append(Bead(i))
        self.updater_list.append(Updater(name='base',
                                         bead_list=self.bases,
                                         osc_client=self.osc_client))

        for i in range(self.CROSS_LED_COUNT):
            self.cross.append(Bead(i))
        self.updater_list.append(Updater(name='cross',
                                         bead_list=self.cross,
                                         osc_client=self.osc_client))


        # some useful predefined sets of beads
        self.set_registry = {
            'none': frozenset(),
            'all': frozenset(self.beads),
            'rosary': frozenset(self.beads),
            'stem': frozenset(self.beads[0:5]),
            'ring': frozenset(self.beads[5:60]),
            'eighth0': frozenset(self.beads[5:11]),
            'eighth1': frozenset(self.beads[11:18]),
            'eighth2': frozenset(self.beads[18:25]),
            'eighth3': frozenset(self.beads[25:32]),
            'eighth4': frozenset(self.beads[32:39]),
            'eighth5': frozenset(self.beads[39:46]),
            'eighth6': frozenset(self.beads[46:53]),
            'eighth7': frozenset(self.beads[53:60]),
            'quadrent0': frozenset(self.beads[5:18]),
            'quadrent1': frozenset(self.beads[18:32]),
            'quadrent2': frozenset(self.beads[32:46]),
            'quadrent3': frozenset(self.beads[46:60]),
            'even_all': frozenset(self.beads[0:60:2]),
            'even_ring': frozenset(self.beads[6:60:2]),
            'odd_all': frozenset(self.beads[1:60:2]),
            'odd_ring': frozenset(self.beads[5:60:2]),
            'base': frozenset(self.bases[0:self.BASE_COUNT]),
            'cross': frozenset(self.cross[0:self.CROSS_LED_COUNT]),
            'lords_prayer': frozenset([self.beads[10], self.beads[21], self.beads[32], self.beads[43], self.beads[54]]),
            'decade0': frozenset(self.beads[5:9] + self.beads[55:59]),
            'decade1': frozenset(self.beads[11:20]),
            'decade2': frozenset(self.beads[22:31]),
            'decade3': frozenset(self.beads[33:42]),
            'decade4': frozenset(self.beads[44:53]),
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
            'white': color.Color(1,1,1,1),
            'tungsten100': color.Color(1, 214/255, 170/255),
            'tungsten40': color.Color(1, 197/255, 143/255),
            'candle': color.Color(1, 147/255, 41/255),
            'fire': color.ColorMapRandomWalk(
                colormap=color.ColorMap(colormap=[
                    color.ColorMapStep(step=0, color=color.Color(1, 132/255, 41/255)),
                    color.ColorMapStep(step=1/6, color=color.Color(1, 137/255, 41/255)),
                    color.ColorMapStep(step=2/6, color=color.Color(1, 142/255, 41/255)),
                    # The middle value here is taken directly from the
                    # "Reproducing Real World Light" article:
                    # http://planetpixelemporium.com/tutorialpages/light.html
                    color.ColorMapStep(step=3/6, color=color.Color(1, 147/255, 41/255)),
                    color.ColorMapStep(step=4/6, color=color.Color(1, 152/255, 41/255)),
                    color.ColorMapStep(step=5/6, color=color.Color(1, 157/255, 41/255)),
                    color.ColorMapStep(step=1, color=color.Color(1, 162/255, 41/255))
                ]),
                time=3
            ),
            'red': color.Color(1,0,0,1),
            'yellow': color.Color(1,1,0,1),
            'green': color.Color(0,1,0,1),
            'blue': color.Color(0,0,1,1),
            'violet': color.Color(1,0,1,1),
            'cyan': color.Color(0,1,1,1),
            # It's annoying when the sim picks black and I can't see anything
            # NOTE YUNFAN: Take this out (maybe) going into prod?
            #'black': color.Color(0,0,0,1)
        }
                                    
        # Automagically register effects so that they're callable by name
        self.register_written_effects()

        # Trigger stuff
        self.register_written_triggers()

        # Map our own exposed methods to the dispatcher
        self.map_to_dispatcher()

        # at the top level we have just one effect: effects.Bin
        # it holds all the other effects.
        self.bin = effects.bin.Bin(self.set_registry['all'], rosary=self)

        self.osc_server = osc_server.ThreadingOSCUDPServer(
            (self.osc_server_ip, self.osc_server_port), self.dispatcher)

    def beads_set_bgcolor(self, beads):
        for bead in beads:
            bead.color.set(self.bgcolor)

    def osc_server_main(self):
        print("Serving on {}".format(self.osc_server.server_address))
        self.osc_server.serve_forever()
    

    ##########################################################################
    # INITIALIZATION STUFF - DISCOVER WRITTEN MODULES
    ##########################################################################
    def register_effect(self, effect):
        """
        Register the name of an effect in our effect registry.  This allows
        us to access the effect without having access to the python
        object name itself.
        """
        # instantiate the object so we get get the name
        e = effect(bead_set=self.set_registry['none'], rosary=self)
        # Argh, because of the way we're doing the above line,
        # trigger_hijacks actually WILL hijack right now, so undo that
        e.unhijack_triggers()
        # note that we are returning effect, a class, not e, an instance!
        self.effect_registry[e.name] = effect


    def find_written_effects(self, module_or_class):
        """
        Look through the filesystem for effect classes
        that people have written.
        """

        classes = set()

        # A little imperfect, as we'll first process imports and
        # we end up trying to add mp.effects.effect.Effect many times
        # We're circumventing this by using a set
        # Inspired by:
        #   http://stackoverflow.com/a/408465
        #   http://stackoverflow.com/a/22578562
        for name, obj in inspect.getmembers(module_or_class):
            if inspect.ismodule(obj) and obj.__package__ == 'mp.effects':
                classes = classes.union(self.find_written_effects(obj))
            elif inspect.isclass(obj):
                classes.add(obj)

        return classes


    def register_written_effects(self):
        """
        Find all the effect that people have written and register them.
        """

        defined_effects = self.find_written_effects(effects)
        for eff in defined_effects:
            # Don't register abstract classes, e.g. effects.effect.Effect
            if not inspect.isabstract(eff) and issubclass(eff, effects.effect.Effect):
                self.register_effect(eff)


    def register_trigger(self, trigger_class):
        """
        Unlike effects, instead of holding on to the init function,
        just go ahead and instantiate the trigger once

        (Maybe reconsider this later)
        """

        # Instantiate
#        self.trigger_id += 1
#        trigger = trigger_class()
#        trigger.rosary = self
#        trigger.id = self.trigger_id
#        self.triggers[trigger.name] = trigger
#
#        self.dispatcher.map(trigger.osc_path,
#                            trigger.trigger_wrapper,
#                            trigger)
        print("REGISTER TRIGGER")
        print(trigger_class)
        t = trigger_class()
        self.trigger_registry[t.name] = trigger_class


    def find_written_triggers(self, module_or_class):
        """
        Crawl through mp.triggers package and find (non-abstract) subclasses
        to register with the rosary
        """

        classes = set()
        for name, obj in inspect.getmembers(module_or_class):
            if inspect.ismodule(obj) and obj.__package__ == 'mp.triggers':
                classes = classes.union(self.find_written_triggers(obj))
            elif inspect.isclass(obj):
                classes.add(obj)

        return classes
        

    def register_written_triggers(self):
        """
        Figure out which triggers are defined in .py files, and register them
        """

        defined_triggers = self.find_written_triggers(triggers)
        for tr in defined_triggers:
            # Don't register abstract classes, e.g. effects.effect.Effect
            if not inspect.isabstract(tr) and issubclass(tr, triggers.trigger.Trigger):
                self.register_trigger(tr)


    ##########################################################################
    # ROSARY CONTROL - RUNTIME HUMAN INTERFACES
    ##########################################################################

    # TODO: HOW MUCH DO I NEED THIS?
    def trigger(self, id):
        for t in self.triggers:
            if t.id == id:
                return t
        return None


    def add_trigger_object(self, trigger):
        """
        When we "fire" a trigger, create a new trigger object like we do for
        effects, then run through its `inner_fire()`, and promptly exit
        """
        self.trigger_id += 1
        trigger.id = self.trigger_id
        trigger.rosary = self
        self.triggers.append(trigger)
        trigger.fire()
        return self.trigger_id


    @dm.expose()
    def add_effect(self, *args, **kwargs):
        """
        Expect kwargs to have all the effect initialization args.
        If it doesn't, fail silently, but gracefully.
        """

        effect_name = kwargs.get('name')
        bead_set_name = kwargs.get('bead_set', 'rosary')
        bead_set_sort = kwargs.get('bead_set_sort', 'cw')

        # Accept either a color name or rgb values
        color_name = kwargs.get('color', 'white')
        r = kwargs.get('r', 0.0)
        g = kwargs.get('g', 0.0)
        b = kwargs.get('b', 0.0)
        a = kwargs.get('a', 0.0)

        # If you don't pass in a good name I'll pretend I didn't hear you
        bead_set = self.set_registry.get(bead_set_name.lower(),
                                         self.set_registry['all'])

        if any([r, g, b]):
            effect_color = color.Color(r, g, b, a)
        else:
            effect_color = self.color_registry.get(color_name.lower())

        # If all else fails, just pick a random color from the registry
        while effect_color in (None, color.Color(0,0,0)):
            effect_color = random.choice(list(self.color_registry.values()))

        # Whether we're overwriting the string or setting for the first time,
        # it's all the same to us
        kwargs['bead_set'] = bead_set
        kwargs['color'] = effect_color
        kwargs['bead_set_sort'] = bead_set_sort

        # I'd rather be fancy and strip out kwargs that won't be accepted
        # than force people writing effects to take **kwargs /flex
        requested_effect = self.effect_registry.get(effect_name)
        requested_effect_args = inspect.getargspec(requested_effect).args
        # I don't want to add this to all the effects that are already written, but this
        # solution feels like a gross hack
        requested_effect_args.append('bead_set_sort')

        # Er, "clean up" the kwargs to pass to an effect init method
        for key in list(kwargs):
            if key not in requested_effect_args:
                kwargs.pop(key)

        if requested_effect is not None:
            effect_id = self.bin.add_effect_object(requested_effect(*args, rosary=self, **kwargs))
            self.expose_effect_knobs(requested_effect)
            return effect_id
        else:
            return None

    @dm.expose()
    def del_effect(self, id):
        self.bin.del_effect(id)

    @dm.expose()
    def clear_effects(self):
        self.bin.clear_effects()
        
    @dm.expose()
    def clear_effects_fade(self):
        """
        Just calling clear_effects() is jarring, let's ease it in
        """

        for eff in self.bin.effects:
            eff.fade_out(30)

    @dm.expose()
    def clear_triggers(self):
        """
        Rudely interrupt any triggers that haven't yet finished
        what they were doing.
        """
        while self.triggers:
            tr = self.triggers[-1]
            self.triggers.remove(tr)

    @dm.expose()
    def start(self, interactive=False):
        """Start the animation loop (aka, mainloop()) and create a shell for live interaction."""
        r = self
        if (r.run_mainloop == False):
            r.run_mainloop = True
            self.t_mainloop = threading.Thread(name='mainloop', target=self.mainloop)
            self.t_mainloop.start()

            self.t_osc_server = threading.Thread(name='osc_server', target=self.osc_server_main)
            self.t_osc_server.start()

            if interactive:
                code.interact(local=locals())

    @dm.expose()
    def stop(self):
        """Stop the mainloop and exit the application."""
        self.run_mainloop = False
        self.osc_server.shutdown()
        exit(0)


    @dm.expose()
    def pause(self):
        """Stop the animation loop without exiting."""
        if (self.run_mainloop):
            self.run_mainloop = False


    @dm.expose()
    def resume(self):
        """Restart the animation loop."""
        self.run_mainloop = True



    ##########################################################################
    # ROSARY MAIN LOOP RELATED - AUTOMATIC EVERY ITERATION
    ##########################################################################
    def unexpose_effect_knobs(self, effect):
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


    def expose_effect_knobs(self, effect):
        """
        Given an effect, create mappings in self.knobs to effect's
        `dm.expose()`-ed functions

        FUN FACT: Why is this here and not on the effect itself?
            - We wanted to play around with decorators
            - Decorators run at "compile-time" and not "run-time"
            - We don't know which knobs an effect has at initilization
            - We need to expose the knobs after the effect is created
            - Our first opportunity is the first mainloop() after
            - This method is called in bin.py's next()
        """

        #if not effect.registered:
        for fn_name, fn in effect.dm.exposed_methods.items():
            if fn_name in self.knobs.keys():
                self.knobs[fn_name].append( (fn, effect) )
            else:
                self.knobs[fn_name] = [ (fn, effect) ]

        effect.registered = True


    def mainloop(self, *args, **kwargs):
        """This is the animiation loop. It cycles through all active effects
        and invokes next() on each effect.

        knobs:
        * frame_time: how much wall-clock time to allocate to each update

        """

        frame_time = kwargs.get('frame_time', self.frame_time)

        next_frame_time = time.monotonic()
        
        # # setup data[] for running average of last 60 time deltas
        # data = []
        # for i in range(60):
        #     data.append(0)

        while (self.run_mainloop):
            next_frame_time += self.frame_time

            bead_list = kwargs.get('bead_list')

            for updater in self.updater_list:
                self.beads_set_bgcolor(updater.bead_list)

            # advance the state of all the effects
            self.bin.next()

            # Let the triggers figure out for themselves what to do
            #for trigger in self.triggers.values():
            #    if trigger.running:
            #        trigger.next()

            # store the time - we will use this to decide how long to sleep
            now = time.monotonic()

            # drop a frame if we've already passed next_frame_time
            while (now > next_frame_time):
                print('frame drop')
                next_frame_time += self.frame_time
                # "dropping a frame" means calling next() on all the effects w/o updating the LEDs
                self.bin.next()

                now = time.monotonic()

            # # compute a running average of the last 60 time deltas
            # if (i == 60):
            #     print(sum(data) / 60)
            #     i = 0
            # data[i] = next_frame_time - now
            # i += 1

            # sleep our estimated drift time
            time.sleep(next_frame_time - now)

            # update the LEDs
            # do this last to try to make the updates as regular as possible
            for updater in self.updater_list:
                updater.update()



    ##########################################################################
    # DEFINE OSC DISPATCHER ROUTES
    ##########################################################################
    def fire_trigger(self, trigger_name, v, **kwargs):

        # See if any currently running effects have hijacked this trigger
        hijacked = self.trigger_hijacks.get(trigger_name)

        if hijacked is not None and len(hijacked) > 0:

            # I thought it'd be cool if the hijacks acted like a stack -
            # if many effects hijack the same trigger, then only the newest
            # effect's hijacked trigger fires
            hijacked_effect, hijacked_method = hijacked[-1]

            print("Trigger {} hijacked by {}".format(trigger_name,
                                                     hijacked_effect))
            hijacked_method(v, **kwargs)

        else:

            requested_trigger = self.trigger_registry.get(trigger_name)
            # I really only expect there to be one trigger running at a time,
            # but just in case, get everyone's names
            running_trigger_names = [t.name for t in self.triggers]

            # Don't want to restart a running trigger
            if requested_trigger is not None and \
               trigger_name not in running_trigger_names:

                # Kill all existing triggers
                self.clear_triggers()

                # Start fading out all existing effects
                self.clear_effects_fade()

                self.add_trigger_object(requested_trigger(*args, **kwargs))


    def turn_knob(self, knob_name, *args, **kwargs):
        """
        For all registered effect instance methods mapped to this knob_name,
        turn the knob (we're assured they're all running effects)
        """

        for fn, instance in self.knobs.get(knob_name, []):
            fn(instance, *args, **kwargs)


    def route_osc_call(self, full_path, *args, **kwargs):
        """
        Figure out what the OSC path means and, well, do what the
        runes instruct us to do.
        """

        print("Route OSC call: {}".format(full_path))

        osc_args = full_path.split('/')
        osc_args.remove('')

        # 'rosary', 'effect', 'trigger', etc.
        namespace = osc_args.pop(0)
        # The actual function name, in that namespace: 'add_effect', etc.
        fn_name = osc_args.pop(0)

        # Finally, the rest of the parsed args are expected to actually
        # represent key/value pairs, so expect there to be an even-numbered
        # count of items
        inferred_kwargs = {}
        for i in range(int(len(osc_args)/2)):
            implied_arg = osc_args[i*2]
            implied_val = osc_args[i*2 + 1]

            # Convert strings representing ints to ints and
            # strings representing floats to floats
            #
            # NOTE: Happily, python will raise a ValueError if we try
            # to cast a float-as-string into an int, instead of just
            # truncating it, phew!
            #
            try:
                implied_val = int(implied_val)
            except ValueError:
                try:
                    implied_val = float(implied_val)
                except ValueError:
                    pass

            inferred_kwargs[implied_arg] = implied_val

        print("* Namespace: {}".format(namespace))
        print("* Function: {}".format(fn_name))
        print("* Inferred kwargs: {}".format(inferred_kwargs))

        # If we have inferred kwargs, use them
        # Otherwise, use whatever is in passed args
        # If nothing, assume a 1 from passed args
        if namespace == 'rosary':
            if fn_name in self.dm.exposed_methods.keys():
                print("* Found rosary function, calling")
                # We expect to mostly end up here
                if inferred_kwargs:
                    self.dm.exposed_methods[fn_name](self, **inferred_kwargs)
                # But in some rare cases, we set some reasonable defaults
                # even if you're being COMPLETELY lazy
                else:
                    self.dm.exposed_methods[fn_name](self, *args)

        elif namespace == 'effect':
            if inferred_kwargs:
                print("* Found effect knob, calling")
                self.turn_knob(fn_name, **inferred_kwargs)
            else:
                self.turn_knob(fn_name, *args)
                
        elif namespace == 'trigger':
            if inferred_kwargs:
                print("* Found trigger, calling")
                self.fire_trigger(fn_name, args[0], **inferred_kwargs)
            else:
                self.fire_trigger(fn_name, args[0])
                
    def map_to_dispatcher(self):
        """
        Register 3 wildcard handlers. But only three. Not THAT wild.

        Less "Wild Things" and more "Where the Wild Things Are."
        """

        self.dispatcher.map("/rosary/*", self.route_osc_call)
        self.dispatcher.map("/effect/*", self.route_osc_call)
        self.dispatcher.map("/trigger/*", self.route_osc_call)
