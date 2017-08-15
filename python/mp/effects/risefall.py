import copy
from mp.effects import effect
from mp import color
import math

class RiseFall(effect.Effect):
    """
    Kinda like Level, but instead of immediately kicking up, rising up
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), speed=1, parabolic=True, once=False, **kwargs):
        super().__init__(name="risefall", bead_set=bead_set, color=color, **kwargs)

        self.speed = speed
        self.speed_delta = 0
        self.parabolic = parabolic
        self.once = once
        self.current = 0

    def next(self):

        for i in range(0, int(round(self.current))):
            self.bead_list[i].color.set(self.color)

        # Could be consolidated, but I don't want an unreadable if/else
        if self.current >= len(self.bead_list) and self.speed > 0:
            self.speed *= -1
            self.speed_delta *= -1
        elif self.current <= 0 and self.speed < 0:
            self.speed *= -1
            self.speed_delta *= -1

            # If we only want this to happen once, don't start back up
            if self.once:
                self.finished = True

        self.current += (self.speed + self.speed_delta)

        # Bounds checking
        if self.current > len(self.bead_list):
            self.current = len(self.bead_list)
        elif self.current < 0:
            self.current = 0

        # (Copy/Pasted from shooter)
        # AW YISS TIME FOR MATH
        if self.parabolic:

            # Er, just...eyeball this number until it looks good enough
            # Lower means less effect on self.speed
            STATIC_SCALAR = .8

            # Normalzie to 0-1 to give to sin function
            normalized_current = self.current / len(self.bead_list)

            speed_delta = self.speed * math.sin( (math.pi/2) * normalized_current)
            # If speed_delta ever reaches speed, things get VERY boring
            speed_delta_capped = min( .99 * abs(self.speed), abs(speed_delta))

            if speed_delta < 0:
                speed_delta_capped = -speed_delta_capped

            # Well actually it's negative because we want to slow down
            self.speed_delta = -(STATIC_SCALAR * speed_delta_capped)

