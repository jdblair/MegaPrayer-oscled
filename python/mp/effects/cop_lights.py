import copy
from mp import color
from mp.effects import effect
from mp.effects import looper
from mp.effects import strobe
from mp import rosary
from mp import effect_list
from mp import color as _color

class CopLights(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), direction=1, **kwargs):
        super().__init__(name="cop_lights", bead_set=bead_set, color=color, **kwargs)

        self.effects = effect_list.EffectList(self.rosary, self.id)
        self.effects.add_effect_object(looper.Looper(bead_set, color=_color.Color(1, 0, 0), length=6))
        self.effects.add_effect_object(looper.Looper(bead_set, color=_color.Color(1, 0, 0), length=6, speed=-0.5))
        self.effects.add_effect_object(looper.Looper(bead_set, color=_color.Color(0, 0, 1), length=6, speed=-0.5, start_offset=20))
        self.effects.add_effect_object(looper.Looper(bead_set, color=_color.Color(0, 0, 1), length=6, start_offset=20))
        self.effects.add_effect_object(strobe.Strobe(bead_set, color=_color.Color(1, 1, 1)))


    def next(self):
        self.effects.next()

    @dm.expose()
    def set_direction(self, direction):
        self.direction = direction
