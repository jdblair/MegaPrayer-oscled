import copy

from mp import color

class Effect:
    """
    Effect is the base class for all effects. It provides properties and methods
    that are common to all Effects.

    The most important of these methods are:

    * set_bead_set(): stores a sorted list in bead_set
    * next(): called every mainloop cycle and should be invoked by every Effect's
      own next() method.
    """
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
        """Returns the name of the Effect."
        return self.name

    def next(self):
        """Invoked for every mainloop cycle. This method _must_ be invoked by every Effect's next() method."""
        self.color.next()

