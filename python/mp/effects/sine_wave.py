import copy
import math

from mp import color
from mp.effects import effect

class SineWave(effect.Effect):
    """Sets the alpha value of a set of beads by mapping a unit circle to
    the beads in the bead_list then computing a sine wave. Each step
    advances the angle by 2 * pi / number of beads.

    knobs:
    * period: the number of sine wave periods in the unit circle (can be float)
    * direction: the distance (positive or negative float) to advance around the unit circle in one mainloop step
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(1,1,1), duration=None, period=1, direction=1):
        super().__init__("sine_wave", bead_set, color=color, duration=duration)
        self.offset = 0
        self.period = period
        self.direction = direction

    def next(self, rosary):
        super().next()
        
        for b in (self.bead_list):
            alpha = (math.sin((2 * math.pi / len(self.bead_list) * self.period) * (b.index + self.offset)) + 1) / 2
            b.color.set(self.color, alpha=alpha)
        self.offset = (self.offset) + self.direction % len(self.bead_list)

    @dm.expose()
    def set_offset(self, offset):
        self.offset = offset

    @dm.expose()
    def set_period(self, period):
        self.period = period

    @dm.expose()
    def set_direction(self, direction):
        self.direction = direction

class ThreePhaseSineWave(effect.Effect):
    """Sets the color of a set of beads by mapping a unit circle
    separately to each of r, g and b in the the beads in the bead_list
    then computing a sine wave. Each step advances the angle by 2 * pi
    / number of beads, offset by a phase argument for each color.

    knobs:
    * period: the number of sine wave periods in the unit circle (can be float)
    * direction: the distance (positive or negative float) to advance around the unit circle in one mainloop step
    * phase_r: phase offset for red
    * phase_g: phase offset for green
    * phase_b: phase offset for blue
    """

    # Wish there were a better way than requiring this every time
    #dm = DispatcherMapper()
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(1,1,1), duration=None, period=1, direction=1):
        super().__init__("3phase_sine_wave", bead_set, color=color, duration=duration)
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

    @dm.expose()
    def set_offset(self, offset):
        self.offset = offset

    @dm.expose()
    def set_period(self, period):
        self.period = period

    @dm.expose()
    def set_direction(self, direction):
        self.direction = direction

    @dm.expose()
    def set_phase_r(self, phase_r):
        self.phase_r = phase_r

    @dm.expose()
    def set_phase_g(self, phase_g):
        self.phase_g = phase_g

    @dm.expose()
    def set_phase_b(self, phase_b):
        self.phase_b = phase_b
