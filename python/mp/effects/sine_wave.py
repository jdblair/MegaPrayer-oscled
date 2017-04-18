import math

from mp.effects import effect
from mp import color

class SineWave(effect.Effect):

    def __init__(self, bead_set, color=color.Color(1,1,1), period=1, direction=1):
        super().__init__("sine_wave", bead_set, color=color)
        self.offset = 0
        self.period = period
        self.direction = direction

    def next(self, rosary):
        super().next()
        
        for b in (self.bead_list):
            intensity = (math.sin((2 * math.pi / len(self.bead_list) * self.period) * (b.index + self.offset)) + 1) / 2
            b.color.set(self.color, intensity)
        self.offset = (self.offset) + self.direction % len(self.bead_list)

class ThreePhaseSineWave(effect.Effect):

    def __init__(self, bead_set, color=color.Color(1,1,1), period=1, direction=1):
        super().__init__("3phase_sine_wave", bead_set, color=color)
        self.offset = 0
        self.period = period
        self.direction = direction
        self.phase_r = 0
        self.phase_g = .25
        self.phase_b = .5

    def next(self, rosary):
        super().next()

        bead_count = len(self.bead_list)
        phase_r = self.phase_r * bead_count
        phase_g = self.phase_g * bead_count
        phase_b = self.phase_b * bead_count

        for bead in (self.bead_list):
            bead.color.r = ((math.sin((2 * math.pi / bead_count * self.period) * (bead.index + self.offset + phase_r)) + 1) / 2) * self.color.r
            bead.color.g = ((math.sin((2 * math.pi / bead_count * self.period) * (bead.index + self.offset + phase_g)) + 1) / 2) * self.color.g
            bead.color.b = ((math.sin((2 * math.pi / bead_count * self.period) * (bead.index + self.offset + phase_b)) + 1) / 2) * self.color.b
        self.offset = (self.offset) + self.direction % bead_count
