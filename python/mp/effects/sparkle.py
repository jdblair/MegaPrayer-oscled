import copy
from mp import color
from mp.effects import effect
import random

class Sparkle(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), duration=None):
        super().__init__("sparkle", bead_set, color=color, duration=duration)
        self.sparkle_time = 6
        self.count = 0

    def next(self, rosary):
        super().next()
        if self.count == 0:
            self.current = random.randint(0,len(self.bead_set) - 1)
            print(self.current)
        if self.count >= self.sparkle_time:
            self.count = 0

        self.bead_list[self.current].color.set(self.color)
        self.count += 1

    @dm.expose()
    def set_direction(self, direction):
        self.direction = direction
