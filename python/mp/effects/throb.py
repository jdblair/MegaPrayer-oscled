import math

from mp.effects import effect

from mp import color

class Throb(effect.Effect):
    """
    Fade the intensity of a set of beads up and down using the specified color.
    The fade is a conventional sine wave.

    knobs:
    * period: number of sine wave periods (corresponds to speed)
    * offset: angle to advance in the sine wave per step, in units of step * pi

    """
    def __init__(self, bead_set, color=color.Color()):
        super().__init__("throb", bead_set, color=color)
        self.x = 0.0
        self.period = 1
        self.step = .05

    def next(self, rosary):
        super().next()

        intensity = (math.sin(self.x * math.pi * self.period) + 1) / 2
        for bead in (self.bead_list):
            bead.color.set(self.color, intensity=intensity)
        self.x += self.step


