from mp.triggers import trigger
from mp import color

class LeftNail(trigger.Trigger):

    def __init__(self):
        super().__init__("left_nail")

        self.effect_sequence = [
            {
                'time': 0,
                'name': 'throb',
                #'args': ['duration', 120]
                'kwargs': {'duration': 60}
            },
            {
                'time': 60,
                'name': 'sine_wave',
                #'args': ['duration', 120]
                'kwargs': {'duration': 120}
            }
        ]

    def trigger(self):
        super().trigger()
        print("HALLO!")
