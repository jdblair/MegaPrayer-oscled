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
                                                   duration=660)
        self.rosary_reveal = random_fill.RandomFill(bead_set=self.rosary.set_registry['rosary'],
                                                    color=_color.Color(1, 1, 1),
                                                    speed=300,
                                                    acceleration=.99,
                                                    delay=100,
                                                    duration=560)
        self.base_reveal = random_fill.RandomFill(bead_set=self.rosary.set_registry['base'],
                                                    color=_color.Color(1, 1, 1),
                                                    speed=200,
                                                    acceleration=.99,
                                                    delay=150,
                                                    duration=510)


        # After the solid white goes away, let it stay dark for a ltitle,
        # then slowly fade it back in
        self.cross_throb = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(1, 1, 1),
                                      step=.01,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=750,
                                      duration=570)
        self.rosary_throb = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(1, 1, 1),
                                      step=.01,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=750,
                                      duration=570)
        self.base_throb = throb.Throb(bead_set=self.rosary.set_registry['base'],
                                      color=_color.Color(1, 1, 1),
                                      step=.01,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=750,
                                      duration=570)

        # After the slow fade goes away, let it stay dark again, for dramatic
        # effect, before returning with a beat
        self.cross_beat = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(1, 1, 1),
                                      step=.125,
                                      offset=(1/math.pi) * -1, # start at 0
                                      duration=120,
                                      delay=1350)
        self.rosary_beat = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(1, 1, 1),
                                      step=.125,
                                      offset=(1/math.pi) * -1, # start at 0
                                      duration=120,
                                      delay=1350)
        self.base_beat = throb.Throb(bead_set=self.rosary.set_registry['base'],
                                      color=_color.Color(1, 1, 1),
                                      step=.125,
                                      offset=(1/math.pi) * -1, # start at 0
                                      duration=120,
                                      delay=1350)

        # Speed it up
        self.cross_beat1 = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(1, 1, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1, # start at 0
                                      duration=210,
                                      delay=1470)
        self.rosary_beat1 = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(1, 1, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1, # start at 0
                                      duration=210,
                                      delay=1470)
        self.base_beat1 = throb.Throb(bead_set=self.rosary.set_registry['base'],
                                      color=_color.Color(1, 1, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1, # start at 0
                                      duration=210,
                                      delay=1470)

        # Add violet to the cross and cyan to the rosary
        self.cross_beat2 = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(1, 0, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1  + math.pi/2,
                                      delay=1560)
        self.rosary_beat2 = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(0, 1, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1  + math.pi/2,
                                      delay=1560)
        self.base_beat2 = throb.Throb(bead_set=self.rosary.set_registry['base'],
                                      color=_color.Color(1, 0, 1),
                                      step=.25,
                                      offset=(1/math.pi) * -1  + math.pi/2,
                                      delay=1560)

        # Now add cyan to the cross and violet to the rosary with
        # retro 80s colors because...
        # Oh why am I explaining myself, everybody loves the 80s
        self.cross_beat3 = throb.Throb(bead_set=self.rosary.set_registry['cross'],
                                      color=_color.Color(0, 1, 1),
                                      step=.5,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=1650)
        self.rosary_beat3 = throb.Throb(bead_set=self.rosary.set_registry['rosary'],
                                      color=_color.Color(1, 0, 1),
                                      step=.5,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=1650)
        self.base_beat3 = throb.Throb(bead_set=self.rosary.set_registry['base'],
                                      color=_color.Color(0, 1, 1),
                                      step=.5,
                                      offset=(1/math.pi) * -1, # start at 0
                                      delay=1650)

        # It seems important that they're grouped like this
        # Otherwise the timing looks off, at least on the sim
        self.bin.add_effect_object(self.cross_reveal)
        self.bin.add_effect_object(self.cross_throb)
        self.bin.add_effect_object(self.cross_beat)
        self.bin.add_effect_object(self.cross_beat1)
        self.bin.add_effect_object(self.cross_beat2)
        self.bin.add_effect_object(self.cross_beat3)

        self.bin.add_effect_object(self.rosary_reveal)
        self.bin.add_effect_object(self.rosary_throb)
        self.bin.add_effect_object(self.rosary_beat)
        self.bin.add_effect_object(self.rosary_beat1)
        self.bin.add_effect_object(self.rosary_beat2)
        self.bin.add_effect_object(self.rosary_beat3)

        self.bin.add_effect_object(self.base_reveal)
        self.bin.add_effect_object(self.base_throb)
        self.bin.add_effect_object(self.base_beat)
        self.bin.add_effect_object(self.base_beat1)
        self.bin.add_effect_object(self.base_beat2)
        self.bin.add_effect_object(self.base_beat3)

    def next(self):
        self.bin.next()
