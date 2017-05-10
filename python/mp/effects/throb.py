import copy
import math

from mp import color
from mp.effects import effect

class Throb(effect.Effect):
    """
    Fade the intensity of a set of beads up and down using the specified color.
    The fade is a conventional sine wave.

    knobs:
    * period: number of sine wave periods (corresponds to speed)
    * offset: angle to advance in the sine wave per step, in units of step * pi

    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), duration=None):
        super().__init__("throb", bead_set, color=color, duration=duration)
        self.x = 0.0
        self.period = 1
        self.step = .05

    def next(self, rosary):
        super().next()

        intensity = (math.sin(self.x * math.pi * self.period) + 1) / 2
        for bead in (self.bead_list):
            bead.color.set(self.color, intensity=intensity)
        self.x += self.step

    @dm.expose()
    def set_period(self, period):
        self.period = period

    @dm.expose()
    def set_step(self, step):
        self.step = step


