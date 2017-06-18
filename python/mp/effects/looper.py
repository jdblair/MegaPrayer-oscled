import copy
from mp.effects import effect
from mp import color

class Looper(effect.Effect):
    """
    Sends a line of beads around in a circle. This makes the most sense with the 'ring' set.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), speed=1, length=1, start_offset=0, **kwargs):
        super().__init__(name="looper", bead_set=bead_set, color=color, **kwargs)
        self.current = start_offset
        self.speed = speed
        self.length = length

        # make sure we don't exceed our limits
        if self.current > len(self.bead_list):
            self.current = len(self.bead_list)
        if self.length > len(self.bead_list):
            self.length = len(self.bead_list)

    def next(self):
        for i in range(0,self.length):
            self.bead_list[(int(round(self.current)) - i) % len(self.bead_list)].color.set(self.color)
        self.current += self.speed
        self.current = self.current % len(self.bead_list)

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed

    @dm.expose()
    def set_length(self, length):
        self.length = length
