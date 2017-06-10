import copy
from mp import color
from mp.effects import effect
from mp.effects import looper
from mp.effects import sparkle
from mp import rosary
from mp import color as _color

class EffectListDemo(effect.Effect):
    """
    A demonstration of a composite effect.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="effect_list_demo", bead_set=bead_set, color=color, **kwargs)

        self.effects = rosary.EffectList(self.rosary)
        self.effects.add_effect_object(looper.Looper(bead_set, color=_color.Color(1, 0, 0), length=5))
        self.effects.add_effect_object(looper.Looper(bead_set, color=_color.Color(0, 1, 0), length=4, speed=-.5))
        self.effects.add_effect_object(sparkle.Sparkle(bead_set, color=_color.Color(1, 1, 1)))

    def next(self):
        self.effects.next()

