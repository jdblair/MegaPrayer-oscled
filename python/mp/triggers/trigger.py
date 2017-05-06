import abc
import copy

from mp import color
from mp.dispatcher_mapper import DispatcherMapper


class Trigger(abc.ABC):
    """
    Effect is the base class for all effects. It provides properties and methods
    that are common to all Effects.

    The most important of these methods are:

    * set_bead_set(): stores a sorted list in bead_set
    * next(): called every mainloop cycle and should be invoked by every Effect's
      own next() method.
    """

    # Can't decorate with @self.r, so need this here
    dm = DispatcherMapper()

    #def __init__(self, name, set, color=color.Color(1,1,1)):
    def __init__(self, name):
        # the name is used when the Effect is registered
        self.name = name
        # id will be assigned when the effect is attached to the mainloop
        self.id = -1
        # the Effect will be removed from effect list if self.finished is true
        self.finished = False
        # Want to be sure that self.rosary exists, even if it's none, see
        # the "register_with_dispatcher" method
        self.rosary = None
        # Since we're not guaranteed a rosary object on init, we will rely
        # on the rosary to call our "register_with_dispatcher" method on every
        # update loop and signal back to the rosary that we did it
        # (p.s. I do like rosary attaching itself to the effect after init)
        self.registered = False

        # A list of effects
        self.effect_sequence = []
        # Fake time
        self.time = 0

        # Effects come and go, but a trigger is forever
        # FOR EV ER
        self.running = False


    def __eq__(self, other):
        return (self.id == other)

    def __repr__(self):
        return "<Trigger:{}: id={}>".format(self.name, self.id)

    def get_name(self):
        """Returns the name of the Effect."""
        return self.name

    @property
    def osc_path(self):
        return "/input/{}".format(self.name)

    def trigger_wrapper(self, unused_addr, hacked_variables, *args, **kwargs):
        return self.trigger()

    @abc.abstractmethod
    def trigger(self):
        """
        Invoked for every mainloop cycle.
        This method _must_ be invoked by every Effect's next() method.
        """

        # If we've been inactive for a while, reset our time
        if not self.running:
            self.running = True
            self.time = 0

    def next(self):
        """
        If we're "running", increment time by 1, check for effects
        """

        print("SELFTIME: {}".format(self.time))

        # Like tears in rain. Time to die.
        if self.running:
            if self.time > max(eff['time'] for eff in self.effect_sequence):
                self.running = False

        for es in self.effect_sequence:
            if es['time'] == self.time:
                self.rosary.add_effect(es['name'], **es['kwargs'])

        self.time += 1
        
        

    def generate_osc_path(self):
        """
        Centralize the dispatcher path name creation
        Unlike for effects, there's only 1 path for a trigger
        """

        return "/{}/trigger/{}/{}".format(self.rosary.name,
                                          self.name,
                                          self.id)

    def register_with_dispatcher(self):
        """
        Make some paths, son
        """
        print("Trigger {} registering following with dispatcher".format(self))
        print(self.dm.registered_methods)

        # If we instantiate an Effect anywhere but in Rosary's add_effect
        # method and then call this, just exit gracefully
        if self.rosary is not None:

            osc_path = self.generate_osc_path()
            self.rosary.dispatcher.map(osc_path,
                                       self.trigger)

            self.registered = True
