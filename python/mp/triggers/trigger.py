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


    def __eq__(self, other):
        return (self.id == other)

    def __repr__(self):
        return "<Trigger:{}: id={}>".format(self.name, self.id)

    def get_name(self):
        """Returns the name of the Trigger. (Does anybody care?)"""
        return self.name

    def pre_fire(self):
        """
        If I want generic stuff to happen for all triggers
        """
        pass

    def post_fire(self):
        """
        Clean up the thing in rosary that prevents the same trigger from
        taking over itself, aka a ghetto debounce
        """
        self.rosary.triggers.remove(self)

    def fire(self):
        self.pre_fire()
        self.inner_fire()
        self.post_fire()

    @abc.abstractmethod
    def inner_fire(self):
        """
        The lengths I go for a pun...
        """
        pass
