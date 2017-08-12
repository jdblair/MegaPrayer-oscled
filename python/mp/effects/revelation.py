import copy
from mp import color as _color
from mp.effects import effect, bin, random_fill, throb, set_color
import math

class Revelation(effect.Effect):
    """
    Random fill the cross, and have the rosary 
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), **kwargs):
        super().__init__(name="revelation", bead_set=bead_set, color=color, **kwargs)

        self.bin = bin.Bin(bead_set=self.rosary.set_registry['cross'],
                           rosary=self.rosary)


        # Use an accelerating random fill to end up with both the cross
        # and the rosary lit up with white
        self.cross_reveal = random_fill.RandomFill(bead_set=self.rosary.set_registry['cross'],
                                                   color=_color.Color(1, 1, 1),
                                                   speed=100,
                                                   acceleration=.99,
                                                   duration=850)
        self.rosary_reveal = random_fill.RandomFill(bead_set=self.rosary.set_registry['rosary'],
                                                    color=_color.Color(1, 1, 1),
                                                    speed=600,
                                                    acceleration=.99,
                                                    delay=50,
                                                    duration=800)


        # After the solid white goes away, let it stay dark for a ltitle,
        # then slowly fade it back in
        self.cross_throb = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(1, 1, 1),
                                      step=.01,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=1000,
                                      duration=500)
        self.rosary_throb = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(1, 1, 1),
                                      step=.01,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=1000,
                                      duration=500)

        # After the slow fade goes away, let it stay dark again, for dramatic
        # effect, before returning with a beat
        self.cross_beat = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(1, 1, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1, # start at 0
                                      duration=300,
                                      delay=1600)
        self.rosary_beat = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(1, 1, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1, # start at 0
                                      duration=300,
                                      delay=1600)

        # Add violet to the cross and cyan to the rosary
        self.cross_beat2 = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(1, 0, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1  + math.pi/2,
                                      delay=1800)
        self.rosary_beat2 = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(0, 1, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1  + math.pi/2,
                                      delay=1800)

        # Now add cyan to the cross and violet to the rosary
        # ...with retro 80s colors!
        self.cross_beat3 = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(0, 1, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=1900)
        self.rosary_beat3 = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(1, 0, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=1900)

        # ADD THAT SHIT IN
        self.bin.add_effect_object(self.cross_reveal)
        self.bin.add_effect_object(self.cross_throb)
        self.bin.add_effect_object(self.cross_beat)
        self.bin.add_effect_object(self.cross_beat2)
        self.bin.add_effect_object(self.cross_beat3)

        self.bin.add_effect_object(self.rosary_reveal)
        self.bin.add_effect_object(self.rosary_throb)
        self.bin.add_effect_object(self.rosary_beat)
        self.bin.add_effect_object(self.rosary_beat2)
        self.bin.add_effect_object(self.rosary_beat3)

    def next(self):
        self.bin.next()
