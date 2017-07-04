import random
from mp.effects import bounce, sine_wave
from mp.triggers import trigger
from mp import color

class LeftNail(trigger.Trigger):
    """
    """

    def __init__(self):
        super().__init__("left_nail")

    def inner_fire(self):
        self.rosary.add_effect(name='shoot',
                               bead_set='stem+left',
                               bead_set_sort='cc',
                               color='white')


class RightNail(trigger.Trigger):
    """
    """

    def __init__(self):
        super().__init__("right_nail")

    def inner_fire(self):
        self.rosary.add_effect(name='shoot',
                               bead_set='stem+right',
                               bead_set_sort='ccw',
                               color='white')

