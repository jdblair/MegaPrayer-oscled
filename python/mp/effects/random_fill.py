import copy
from mp import color
from mp.effects import effect
import random

class RandomFill(effect.Effect):
    """
    Illuminate all the beads in a set by choosing random beads to turn on.

    knobs:
    * speed: number of frames the bead should be illuminated
    * size: number of beads to illuminate at a time
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), duration=None, size=1, speed=2):
        super().__init__("random_fill", bead_set, color=color, duration=duration)
        self.speed = speed
        self.size = size
        self.count = 0
        self.remaining = set(bead_set)
        random.seed()
        self.current = set()

    def next(self, rosary):
        super().next()

        if (len(self.remaining) > 0):
            if self.count >= self.speed:
                self.count = 0
            if self.count == 0:
                for b in random.sample(self.remaining, self.size):
                    self.current.add(b)
                    self.remaining.remove(b)

        for b in self.current:
            b.color.set(self.color)
        
        self.count += 1

    @dm.expose()
    def set_size(self, size):
        self.size = size

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed
