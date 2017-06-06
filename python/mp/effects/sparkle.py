import copy
from mp import color
from mp.effects import effect
import random

class Sparkle(effect.Effect):
    """
    Blink one more randomly chosen beads.

    knobs:
    * frames: number of frames the bead should be illuminated
    * size: number of beads to illuminate
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), duration=None):
        super().__init__("sparkle", bead_set, color=color, duration=duration)
        self.frames = 2
        self.size = 1
        self.count = 0
        self.bead_set = bead_set
        random.seed()

    def next(self, rosary):
        super().next()

        if self.count >= self.frames:
            self.count = 0

        if self.count == 0:
            self.current = random.sample(self.bead_set, self.size)

        for b in self.current:
            b.color.set(self.color)
        
        self.count += 1

    @dm.expose()
    def set_size(self, size):
        self.size = size

    @dm.expose()
    def set_frames(self, frames):
        self.frames = frames
