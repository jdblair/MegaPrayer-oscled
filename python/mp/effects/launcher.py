import copy
from mp.effects import effect, bin, looper
from mp import color

class Launcher(effect.Effect):
    """
    This effect wraps looper and manipulates the bead_set so the moving LED appears to travel
    down the stem the begin looping in the ring.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), speed=1, length=1, start_offset=0, **kwargs):
        super().__init__(name="launcher", bead_set=bead_set, color=color, **kwargs)

        self.my_bead_set = bead_set
        self.looper = looper.Looper(bead_set, color=color, speed=speed, length=length, **kwargs)
        self.in_stem = True

    def next(self):
        self.looper.next()
        # this operation removes the stem from the set after self.current
        # has exited the stem
        if (self.in_stem and
            self.bead_list[self.looper.current] not in self.rosary.set_registry['stem']):
            self.looper.set_bead_set(self.my_bead_set - self.rosary.set_registry['stem'])
            self.in_stem = False
            self.looper.current = 0
