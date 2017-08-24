import copy
from mp.effects import effect
from mp import color

class Sweep(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), speed=1, **kwargs):
        super().__init__(name="sweep", bead_set=bead_set, color=color, **kwargs)
        self.current = 0
        self.speed = speed

    def next(self):
        for i in range(0, int(round(self.current))):
            self.bead_list[i].color.set(self.color)

        self.current += self.speed
        if (self.current > len(self.bead_list)):
            self.finished=True

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed
