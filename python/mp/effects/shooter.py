import copy
from mp import color
from mp.effects import effect

class Shooter(effect.Effect):
    """
    "Shoots" a light one time across the specified set.

    knobs:
    * speed: the amount to move every time tick, can be a float.
             negative values mean counter-clockwise
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)
    
    def __init__(self, bead_set, color=color.Color(), speed=1, length=1, **kwargs):
        super().__init__(name="shooter", bead_set=bead_set, color=color, **kwargs)
        self.speed = speed
        self.length = length
        if self.length > len(self.bead_list):
            self.length = len(self.bead_list)
        if self.speed < 0:
            self.current = len(self.bead_list) - 1
        else:
            self.current = self.length

    def next(self):
        for i in range(0,self.length):
            self.bead_list[int(round(self.current - i))].color.set(self.color)
        self.current += self.speed
        if (self.current > (len(self.bead_list) - 1) or self.current < self.length):
            self.finished = True

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed
