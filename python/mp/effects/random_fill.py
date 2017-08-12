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

    def __init__(self, bead_set, color=color.Color(), duration=None, size=1, speed=2, acceleration=None, **kwargs):
        super().__init__(name="random_fill", bead_set=bead_set, color=color, duration=duration, **kwargs)
        self.speed = speed
        self.size = size
        # It gets pretty tedious waiting for this thing to finish
        # Also it seems lower numbers 0...1 are faster
        self.acceleration = acceleration
        self.count = 0
        self.remaining = set(bead_set)
        random.seed()
        self.current = set()

    def next(self):
        super().next()

        if (len(self.remaining) > 0):
            if self.count >= self.speed:
                self.count = 0
            if self.count == 0:

                # Since we can't go below a speed of 1, if the acceleration
                # takes our speed below 1, instead start increasing size
                if self.speed < 1:
                    accelerated_size = int(self.size * (1 / self.speed))
                else:
                    accelerated_size = self.size

                # Avoid sampling larger than the population
                for b in random.sample(self.remaining, min(len(self.remaining), accelerated_size)):
                    self.current.add(b)
                    self.remaining.remove(b)

        for b in self.current:
            b.color.set(self.color)
        
        self.count += 1

        if self.acceleration is not None:
            self.speed *= self.acceleration

    @dm.expose()
    def set_size(self, size):
        self.size = size

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed
