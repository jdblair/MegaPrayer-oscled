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

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="throb", bead_set=bead_set, color=color, **kwargs)
        self.x = 0.0
        self.period = 1
        self.step = .05

    def next(self):
        super().next()

        alpha = (math.sin(self.x * math.pi * self.period) + 1) / 2
        for bead in (self.bead_list):
            bead.color.set(self.color, alpha=alpha)
        self.x += self.step

    @dm.expose()
    def set_period(self, period):
        self.period = period

    @dm.expose()
    def set_step(self, step):
        self.step = step


