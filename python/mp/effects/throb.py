import math

from mp.effects import effect
from mp import color

class Throb(effect.Effect):
    def __init__(self, bead_set, color=color.Color()):
        super().__init__("throb", bead_set, color=color)
        self.x = 0.0
        self.period = 1

    def next(self, rosary):
        super().next()

        intensity = (math.sin(self.x * math.pi * self.period) + 1) / 2
        for bead in (self.bead_list):
            bead.color.set(self.color, intensity=intensity)
        self.x += 0.05


