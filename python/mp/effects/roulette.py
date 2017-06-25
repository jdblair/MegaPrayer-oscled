import copy
from mp import color as _color
from mp.effects import effect, bin, wheel, looper

class Roulette(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), direction=1, **kwargs):
        super().__init__(name="roulette", bead_set=bead_set, color=color, **kwargs)

        #ring_set = self.rosary.set_registry('ring') & bead_set
        length = 2

        self.bin = bin.Bin(bead_set, rosary=self.rosary)
        self.wheel = wheel.Wheel(bead_set, colors=[_color.Color(1, 0, 0), _color.Color(0, 0, 0)], length=length, speed=0)
        self.looper = looper.Looper(bead_set, color=_color.Color(0, 1, 0), length=length, speed=0, start_offset=1)
        self.bin.add_effect_object(self.wheel)
        self.bin.add_effect_object(self.looper)

        self.set_speed(0.5)

    def next(self):
        self.bin.next()

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed
        self.wheel.speed = speed
        self.looper.speed = speed
