import abc
import copy

from mp import color

class DispatcherMapper:

    def __init__(self):
        self.registered_methods = {}

    def expose(self):
        def decorator(fn):
            self.registered_methods[fn.__name__] = fn
            return fn
        return decorator

    def invoke_exposed(self, unused_addr, hacked_variables, *args, **kwargs):

        print("Handling endpoint: {}".format(unused_addr))
        print("Function definitions: {}".format(hacked_variables))
        print("Arguments from OSC: {}".format(args))

        fn_name = hacked_variables[0]
        effect_obj = hacked_variables[1]
        self.registered_methods[fn_name](effect_obj, *args, **kwargs)


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
        # Magically make paths OH BABY
        self.rosary = None
        #self.register_methods()
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
        #print("SELF? {}, {}".format(self, type(self)))
        #print("SET COLOR TO: {}, {}, {}".format(r, g, b))
        #print("TYPES: {}, {}, {}".format(type(r), type(g), type(b)))
        self.color = color.Color(r, g, b)

    @dm.expose()
    def set_duration(self, sec):
        self.duration = sec

    def register_with_dispatcher(self):
        """
        Make some paths, son
        """
        print("Effect {} registering following with dispatcher".format(self))
        print(self.dm.registered_methods)

        if self.rosary is not None:
            for fn_name in self.dm.registered_methods.keys():

                print("/effect/{}/{}/{}".format(self.rosary.name,
                                                self.id, fn_name))

                self.rosary.dispatcher.map("/effect/{}/{}/{}".format(
                                               self.rosary.name,
                                               self.id,
                                               fn_name),
                                           self.dm.invoke_exposed, fn_name, self)
            self.registered = True
