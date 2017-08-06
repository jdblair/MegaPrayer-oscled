import copy
from mp.effects import effect
from mp import color as _color

class Ramp(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), speed=1, length=1, start_offset=0, **kwargs):
        super().__init__(name="ramp", bead_set=bead_set, color=color, **kwargs)
        
        if len(bead_set) == 0:
            self.r_delta = 0
            self.g_delta = 0
            self.b_delta = 0
            self.a_delta = 0
        else:
            self.r_delta = (self.color.r - self.rosary.bgcolor.r) / len(self.bead_list)
            self.g_delta = (self.color.g - self.rosary.bgcolor.g) / len(self.bead_list)
            self.b_delta = (self.color.b - self.rosary.bgcolor.b) / len(self.bead_list)
            self.a_delta = (self.color.a - self.rosary.bgcolor.a) / len(self.bead_list)

        self.ramp_color = _color.Color()
        self.ramp_color.set(self.rosary.bgcolor)

    def next(self):
        for bead in self.bead_list:
            bead.color.set(self.ramp_color)
            self.ramp_color.r += self.r_delta
            self.ramp_color.g += self.g_delta
            self.ramp_color.b += self.b_delta
            self.ramp_color.a += self.a_delta
    
