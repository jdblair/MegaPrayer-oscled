from mp.triggers import trigger
from mp import color

class SomeOtherThing(trigger.Trigger):
    """
    I'll replace this with more useful documentation
    when I'm done patting myself on the back
    """

    def __init__(self):
        super().__init__("some_other_thing")

    def set_effect_sequence(self):
        return [
            {
                'time': 0,
                'name': 'throb',
                'kwargs': {'duration': 30,
                           'color_name_or_r': 'red'}
            },
            {
                'time': 30,
                'name': 'throb',
                'kwargs': {'duration': 30,
                           'color_name_or_r': 'green'}
            },
            {
                'time': 60,
                'name': 'throb',
                'kwargs': {'duration': 30,
                           'color_name_or_r': 'blue'}
            },
            {
                'time': 90,
                'name': 'throb',
                'kwargs': {'duration': 30,
                           'color_name_or_r': 'yellow'}
            },
            {
                'time': 120,
                'name': 'throb',
                'kwargs': {'duration': 30,
                           'color_name_or_r': 'violet'}
            },
            {
                'time': 150,
                'name': 'throb',
                'kwargs': {'duration': 30,
                           'color_name_or_r': 'cyan'}
            },
            {
                'time': 180,
                'name': 'sine_wave',
                'kwargs': {'duration': 180}
            }
        ]
