import random
from mp.effects import bounce, sine_wave
from mp.triggers import trigger
from mp import color

class LeftNail(trigger.Trigger):
    """
    I'll replace this with more useful documentation
    when I'm done patting myself on the back
    """

    def __init__(self):
        super().__init__("left_nail")

    def inner_fire(self):

        bounce1 = bounce.Bounce(self.rosary.set_registry.get('all'),
                                color.Color(1.0, 0.5, 0.7),
                                rosary=self.rosary,
                                duration=120)
        # Shitty hack
        bounce1.id = random.randrange(1000, 9999)

        bounce2 = bounce.Bounce(self.rosary.set_registry.get('all'),
                                color.Color(0.8, 0.3, 0.5),
                                rosary=self.rosary,
                                duration=117,
                                delay=3)
        bounce2.id = random.randrange(1000, 9999)

        bounce3 = bounce.Bounce(self.rosary.set_registry.get('all'),
                                color.Color(0.8, 0.3, 0.5),
                                rosary=self.rosary,
                                duration=114,
                                delay=6)
        bounce3.id = random.randrange(1000, 9999)

        sinewav = sine_wave.SineWave(self.rosary.set_registry.get('all'),
                                     color.Color(0.0, 0.3, 0.3),
                                     rosary=self.rosary,
                                     duration=120,
                                     delay=75)
        sinewav.id = random.randrange(1000, 9999)

        threeps = sine_wave.ThreePhaseSineWave(self.rosary.set_registry.get('all'),
                                               color.Color(1.0, 1.0, 1.0),
                                               rosary=self.rosary,
                                               duration=180,
                                               delay=210)
        threeps.id = random.randrange(1000, 9999)


        self.rosary.add_effect_object(bounce1)
        self.rosary.add_effect_object(bounce2)
        self.rosary.add_effect_object(bounce3)
        self.rosary.add_effect_object(sinewav)
        self.rosary.add_effect_object(threeps)


class RightNail(LeftNail):
    """
    Lol I'm lazy

    (Also I can't pass direction to rosary.add_effect() right now)
    """

    def __init__(self):
        super(LeftNail, self).__init__("right_nail")
