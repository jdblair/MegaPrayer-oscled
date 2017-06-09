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

    def __init__(self, *args, **kwargs):

        # Introducting...the option to pass a rosary on init instead of
        # assigning it afterwards
        self.rosary = kwargs.get('rosary')
        # the name is used when the Effect is registered
        self.name = kwargs.get('name')
        # the bead_set is a list of beads the Effect is applied to. The order is important!
        self.bead_set = self.set_bead_set(kwargs.get('bead_set', set()))
        # The color of the Effect. This is not always meaningful.
        self.color = kwargs.get('color')
        self.duration = kwargs.get('duration')
        self.delay = kwargs.get('delay', 0)

        # For the purposes of `fade_out` and `duration`
        self.time = 0
        # id will be assigned when the effect is attached to the mainloop
        self.id = -1
        # the Effect will be removed from effect list if self.finished is true
        self.finished = False
        # Since we're not guaranteed a rosary object on init, we will rely
        # on the rosary to look at our exposed methods (via `@dm.expose())
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

    def set_bead_set_cc(self, set):
        """Convenience function for storing a set of beads as a sorted list in
        a counter-clockwise direction."""
        bead_map = [0, 1, 2, 3, 4,
                    59, 58, 57, 56, 55, 54, 53, 52, 51, 50,
                    49, 48, 47, 46, 45, 44, 43, 42, 41, 40,
                    39, 38, 37, 36, 35, 34, 33, 32, 31, 30,
                    29, 28, 27, 26, 25, 24, 23, 22, 21, 20,
                    19, 18, 17, 16, 15, 14, 13, 12, 11, 10,
                    9, 8, 7, 6, 5]

        beads = []
        for bead in set:
            beads.append(bead)
        beads.sort(key=lambda bead: bead_map[bead.index])
        self.bead_list = beads

    def get_name(self):
        """Returns the name of the Effect."""
        return self.name

    def supernext(self):
        """
        Invoked for every mainloop cycle.

        Having the rosary call this method, and having this method call
        the actual `next()` method lets me make generically implement `delay`
        without forcing every effect to re-implement it.
        """

        # In refactoring triggers, I wanted an alternate way to "script"
        # sequences - if delay is passed, don't start "nexting" until it's over
        if self.time > self.delay:
            self.color.next()
            self.next()

        if self.duration is not None and self.time >= self.duration + (self.delay or 0):
            self.rosary.del_effect(self.id)

        self.time += 1

    @abc.abstractmethod
    def next(self):
        """
        This method _must_ be invoked by every Effect's next() method.
        """
        pass

    @dm.expose()
    def set_color(self, r, g, b):
        self.color = color.Color(r, g, b)

    @dm.expose()
    def set_duration(self, sec):
        self.duration = sec

    @dm.expose()
    def fade_out(self, fade_duration):
        self.color = color.ColorFade(self.color, color.Color(0,0,0), fade_duration)
        # Begin countdown to self-destruction
        self.duration = self.delay + self.time + fade_duration
