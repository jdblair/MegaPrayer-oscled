import copy
from mp import color
from mp.effects import effect
import math

class Shooter(effect.Effect):
    """
    "Shoots" a light one time across the specified set.

    knobs:
    * speed: the amount to move every time tick, can be a float.
             negative values mean counter-clockwise
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)
    
    def __init__(self, bead_set, color=color.Color(), speed=1, length=1, parabolic=False, **kwargs):
        super().__init__(name="shooter", bead_set=bead_set, color=color, **kwargs)
        self.speed = speed
        self.length = length
        self.parabolic = parabolic
        self.speed_delta = 0
        if self.length > len(self.bead_list):
            self.length = len(self.bead_list)
        if self.speed < 0:
            self.current = len(self.bead_list) - 1
        else:
            self.current = self.length

    def next(self):
        for i in range(0,self.length):
            self.bead_list[int(round(self.current - i))].color.set(self.color)

        # Only ever slow down from passed speed, excpect negative acceleration
        self.current += self.speed + self.speed_delta

        if (self.current > (len(self.bead_list) - 1) or self.current < self.length):
            self.finished = True

        # AW YISS TIME FOR MATH
        if self.parabolic:

            # Er, just...eyeball this number until it looks good enough
            # Lower means less effect on self.speed
            STATIC_SCALAR = .9

            # Normalzie to 0-1 to give to sin function
            normalized_current = self.current / len(self.bead_list)

            speed_delta = self.speed * math.sin(math.pi * normalized_current)
            # If speed_delta ever reaches speed, things get VERY boring
            speed_delta_capped = min( .99 * self.speed, speed_delta)
            # Well actually it's negative because we want to slow down
            self.speed_delta = -(STATIC_SCALAR * speed_delta_capped)

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed
