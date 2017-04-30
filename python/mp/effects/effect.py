import abc
import copy

from mp import color
from mp.dispatcher_mapper import DispatcherMapper


class Effect(abc.ABC):
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

    def __init__(self, name, set, color=color.Color(1,1,1)):
        # the name is used when the Effect is registered
        self.name = name
        # the bead_set is a list of beads the Effect is applied to. The order is important!
        self.bead_set = self.set_bead_set(set)
        # The color of the Effect. This is not always meaningful.
        self.color = copy.copy(color)
        self.duration = 0
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

    def __eq__(self, other):
        return (self.id == other)

    def __repr__(self):
        return "<Effect:{}: id={}>".format(self.name, self.id)
        
    def set_bead_set(self, set):
        """Convenience function for storing a set of beads as a sorted list."""
        beads = []
        for bead in set:
            beads.append(bead)
        beads.sort(key=lambda bead: bead.index)
        self.bead_list = beads

    def get_name(self):
        """Returns the name of the Effect."""
        return self.name

    @abc.abstractmethod
    def next(self):
        """
        Invoked for every mainloop cycle.
        This method _must_ be invoked by every Effect's next() method.
        """
        self.color.next()

    @dm.expose()
    def set_color(self, r, g, b):
        self.color = color.Color(r, g, b)

    @dm.expose()
    def set_duration(self, sec):
        self.duration = sec

    def generate_osc_path(self, fn_name):
        """
        Centralize the dispatcher path name creation
        """

        return "/{}/effect/{}/{}".format(self.rosary.name,
                                         self.id,
                                         fn_name)

    def register_with_dispatcher(self):
        """
        Make some paths, son
        """
        print("Effect {} registering following with dispatcher".format(self))
        print(self.dm.registered_methods)

        # If we instantiate an Effect anywhere but in Rosary's add_effect
        # method and then call this, just exit gracefully
        if self.rosary is not None:
            for fn_name in self.dm.registered_methods.keys():

                osc_path = self.generate_osc_path(fn_name)
                print(osc_path)

                self.rosary.dispatcher.map(osc_path,
                                           self.dm.invoke_exposed,
                                           fn_name,
                                           self)
            self.registered = True
