import copy
from mp import color as _color
from mp.effects import effect, bin, looper, strobe

class CopLights(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), direction=1, **kwargs):
        super().__init__(name="cop_lights", bead_set=bead_set, color=color, **kwargs)

        self.bin = bin.Bin(bead_set, rosary=self.rosary)
        self.bin.add_effect_object(looper.Looper(bead_set, color=_color.Color(1, 0, 0), length=6))
        self.bin.add_effect_object(looper.Looper(bead_set, color=_color.Color(1, 0, 0), length=6, speed=-0.5))
        self.bin.add_effect_object(looper.Looper(bead_set, color=_color.Color(0, 0, 1), length=6, speed=-0.5, start_offset=20))
        self.bin.add_effect_object(looper.Looper(bead_set, color=_color.Color(0, 0, 1), length=6, start_offset=20))
        self.bin.add_effect_object(strobe.Strobe(bead_set, color=_color.Color(1, 1, 1)))


    def next(self):
        self.bin.next()

    @dm.expose()
    def set_direction(self, direction):
        self.direction = direction
