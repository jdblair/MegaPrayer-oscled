import copy
from mp import color
from mp.effects import effect

class Bounce(effect.Effect):
    """
    Bounce colors a single bead, one at a time, from the lowest bead to
    the highest bead. Once the high bead is reached the direction
    reverses until the low bead is reached.

    self.direction is a positive or negative integer.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), duration=None, direction=1):
        super().__init__("bounce", bead_set, color=color, duration=duration)
        self.direction = direction
        if (self.direction < 0):
            self.current = len(self.bead_list) - 1
        else:
            self.current = 0
        self.last = self.current

    def next(self, rosary):
        super().next()

        # self.bead_list[self.last].color.set(rosary.bgcolor)
        self.current += self.direction
        self.last = self.current
        self.bead_list[self.current].color.set(self.color)
        if (self.current >= (len(self.bead_list) - 1) or self.current <= 0):
            self.direction *= -1

    @dm.expose()
    def set_direction(self, direction):
        print("OH SHIT I WAS TOLD TO SET DIRECTION")
        self.direction = direction
