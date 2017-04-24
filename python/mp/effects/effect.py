import abc
import copy

from mp import color

class Registerer:

    def __init__(self):
        self.registered_methods = {}

    def decorated(self):
        print("DECORATED")
        def decorator(fn):
            print("DECORATOR")
            print(fn)

            #def newfn(unused_addr, blargs, *args, **kwargs):
            #    fn(*args, **kwargs)

            #self.registered_methods[fn.__name__] = newfn
            self.registered_methods[fn.__name__] = fn

            return fn
        return decorator

    def soldier(self, unused_addr, blargs, *args, **kwargs):
        print("UNUSED ADDR: {}".format(unused_addr))
        name = blargs[0]
        print("NAME: {}".format(name))
        print("*ARGS: {}".format(args))
        self.registered_methods[name](*args)

def christmas(dispatcher):
    print("CHRISTMAS")
    def decorated_fn(fn, *args, **kwargs):
        print("DECORATOR")
        print(dispatcher)
        print(fn)
        #jself.rosary.dispatcher.map("/effect/{}/{}/{}".format(
        #j                               self.rosary.name,
        #j                               self.id,
        #j                               k),
        #j                           fn)
        #jfn(*args, **kwargs)
        return fn

    return decorated_fn

class Effect(abc.ABC):
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


    r = Registerer()

    #@christmas(dispatcher)
    @r.decorated()
    #def set_color(self, unused_addr, args, r, g, b):
    def set_color(self, r, g, b):
        print("SELF? {}, {}".format(self, type(self)))
        print("SET COLOR TO: {}, {}, {}".format(r, g, b))
        print("TYPES: {}, {}, {}".format(type(r), type(g), type(b)))
        self.color = color.Color(r, g, b)

    def register_methods(self):
        """
        Make some paths, son
        """
        print("REGISTER METHODS!")
        print(self.r.registered_methods)

        if self.rosary is not None:
            for k, v in self.r.registered_methods.items():
                print("/effect/{}/{}/{}".format(self.rosary.name, self.id, k))
                print(k)
                print(v)
                self.rosary.dispatcher.map("/effect/{}/{}/{}".format(
                                               self.rosary.name,
                                               self.id,
                                               k),
                                           #v)
                                           self.r.soldier, k)
            self.registered = True
        

    def test_register_methods(self):
        if self.rosary is not None:
            print("/effect/{}/{}/color".format(self.rosary.name, self.id))
            self.rosary.dispatcher.map("/effect/{}/{}/color".format(
                                           self.rosary.name,
                                           self.id),
                                       self.set_color, "Red", "Green", "Blue")
            self.registered = True
