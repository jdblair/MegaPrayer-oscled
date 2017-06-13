import copy
import math

from mp import color
from mp.effects import effect

class VibrationFixed(effect.Effect):
    """
    Implement the formula for vibration on a fixed string.
    y(x,t) = ym * sin(kx - wt) + ym * sin(kx + wt)

    see http://www.acs.psu.edu/drussell/Demos/string/Fixed.html
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(1,1,1), duration=None, ym=1, k=.25, w=1, **kwargs):
        super().__init__(name='vibration_fixed', bead_set=bead_set, color=color, duration=duration)
        self.ym = ym
        self.k = k
        self.w = w
        self.t = 0
        self.max = 0
        self.min = 0
        self.t = 0

    def next(self):
        super().next()
        
        for b in (self.bead_list):
            intensity = (((self.ym * math.sin(self.k * b.index - self.w * self.t)) + (self.ym * math.sin(self.k * b.index + self.w * self.t))) + 2) / 4
            b.color.set(self.color, intensity)
            # if self.max < intensity:
            #     self.max = intensity
            #     print("max", self.max)
            # if self.min > intensity:
            #     self.min = intensity
            #     print("min", self.min)
            self.t += 0.01


