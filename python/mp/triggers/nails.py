from mp.triggers import trigger
from mp import color

class LeftNail(trigger.Trigger):
    """
    I'll replace this with more useful documentation
    when I'm done patting myself on the back
    """

    def __init__(self):
        super().__init__("left_nail")

    def set_effect_sequence(self):
        return [
            {
                'time': 0,
                'name': 'bounce',
                'kwargs': {'duration': 120,
                           'color_name_or_r': 1, 'g': .5, 'b': .7}
            },
            {
                'time': 3,
                'name': 'bounce',
                'kwargs': {'duration':117,
                           'color_name_or_r': .8, 'g': .3, 'b': .5}
            },
            {
                'time': 6,
                'name': 'bounce',
                'kwargs': {'duration': 116,
                           'color_name_or_r': .6, 'g': .1, 'b': .3}
            },
            {
                'time': 75,
                'name': 'sine_wave',
                'kwargs': {'duration': 120,
                           'color_name_or_r': 0, 'g': .3, 'b': .3}
            },
            {
                'time': 210,
                'name': '3phase_sine_wave',
                'kwargs': {'duration': 180,
                           'color_name_or_r': 'white'}
            }
        ]

class RightNail(LeftNail):
    """
    Lol I'm lazy

    (Also I can't pass direction to rosary.add_effect() right now)
    """

    def __init__(self):
        super(LeftNail, self).__init__("right_nail")
