import abc
import copy

from mp import color


class Trigger(abc.ABC):
    """
    Trigger is the base class for all triggers.

    Triggers by their nature have less customizing than effects.
    You're really only expected to define the effect_sequence in any subclass.

    * effect_sequence[]: a list of dictionary objects defining what effects
                         should 
    """

    def __init__(self, name):

        # Informs the OSC path naming, otherwise not very useful here
        self.name = name

        # Technically used to compare one trigger to another
        self.id = -1

        # Used to indirectly access effects
        self.rosary = None

        # The trigger() method will reset this to 0 every time we
        # go through the sequence
        self.time = 0

        # This should follow self.time until we stop triggering
        self.last_trigger = 0

        # How many ticks are allowed to pass between last_trigger and time
        # before we decide we've lost the signal
        self.fade_out_threshold = 30.0

        # How many "ticks" between losing the trigger and killng the effects
        self.fade_out_duration = 30.0

        # Effects come and go, but a trigger is forever. FOR EV ER.
        # The only difference is if we're currently running or not
        self.running = False

        # A list of effects
        self.effect_sequence = self.set_effect_sequence()


    def __eq__(self, other):
        return (self.id == other)

    def __repr__(self):
        return "<Trigger:{}: id={}>".format(self.name, self.id)

    def get_name(self):
        """Returns the name of the Trigger. (Does anybody care?)"""
        return self.name

    @abc.abstractmethod
    def set_effect_sequence(self):
        pass

    @property
    def osc_path(self):
        """
        Unlike effects, which might have a variable number of "knobs" any
        trigger will only have one endpoint.

        Furthermore, the rosary will instantiate one of every trigger on its
        own init, so we're not responsible for it here
        """
        return "/input/{}".format(self.name)

    def trigger_wrapper(self, unused_addr, hacked_variables, *args, **kwargs):
        """
        Give this method to the dispatcher to map to the endpoint.

        There's a bunch of stuff that pythonosc.dispatcher.Dispatcher will
        pass back to us that we won't care about
        """
        return self.trigger()

    #@abc.abstractmethod
    def trigger(self):
        """
        Every call to trigger() is a call to next()...
        """

        # If we've been inactive for a while, reset our time
        if not self.running:
            self.running = True
            self.time = 0

        self.last_trigger = self.time


    def next(self):
        """
        ...But not every call to next() is a call to trigger().

        e.g. We'll have to call next() a few times during the fade out
        """

        # If we either:
        #   1) Have reached the end of the sequence
        #   2) Are done fading out
        # Then tell all the effects to remove themselves
        max_effect_time = max(eff['time'] for eff in self.effect_sequence)
        last_effect = next(e for e in self.effect_sequence if e['time'] == \
                           max_effect_time)

        # If we lost the signal, tell all currently running effects to
        # start fading out (ONLY DO THIS ONCE!)
        if (self.time - self.last_trigger == self.fade_out_threshold) or \
           (last_effect['time'] + last_effect['kwargs']['duration'] - \
            self.time == self.fade_out_threshold):

            for es in self.effect_sequence:
                # If we hadn't added the effect yet, this wouldn't exist
                effect_id = es.get('effect_id')

                # Sneakily replace the effect's color property with
                # a color.ColorFade object
                if effect_id is not None:
                    eff = self.rosary.effect(effect_id)
                    if eff is not None:
                        eff.fade_out(self.fade_out_duration)

        if (self.time > last_effect['time'] + last_effect['kwargs']['duration']) or \
           (self.time > self.last_trigger + self.fade_out_threshold + self.fade_out_duration):

            # Marking ourself as "not running" makes self.rosary not call
            # our next()
            self.running = False

            for es in self.effect_sequence:
                # If we hadn't added the effect yet, this wouldn't exist
                effect_id = es.get('effect_id')

                # Each effect will naturally call this in its own next(),
                # but this should be fine as subsequent calls will just
                # do nothing
                if effect_id is not None:
                    self.rosary.del_effect(effect_id)


        # Don't add any new effects if we're fading out
        if self.time - self.last_trigger < self.fade_out_threshold:
            for es in self.effect_sequence:
                if es['time'] == self.time:
                    eff = self.rosary.add_effect(name=es['name'], **es['kwargs'])
                    es['effect_id'] = eff

        self.time += 1
