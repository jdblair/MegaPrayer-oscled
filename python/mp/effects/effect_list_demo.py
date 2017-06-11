import copy

from mp import color
from mp.effects import effect
from mp.effects import looper
from mp.effects import sparkle
from mp import rosary
from mp import effect_list
from mp import color as _color

class EffectListDemo(effect.Effect):
    """
    A demonstration of a composite effect.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="effect_list_demo", bead_set=bead_set, color=color, **kwargs)

        self.count = 0
        self.effects = effect_list.EffectList(self.rosary, self.id)
        self.looper1 = looper.Looper(bead_set, color=_color.Color(1, 0, 0), length=5, speed=0)
        self.effects.add_effect_object(self.looper1)
        self.effects.add_effect_object(looper.Looper(bead_set, color=_color.Color(0, 1, 0), length=4, speed=-.5))
        self.effects.add_effect_object(sparkle.Sparkle(bead_set, color=_color.Color(1, 1, 1)))
        self.speed_increment = .02

    def next(self):
        self.effects.next()

        # looper1 will go faster and slower, increasing and decreasing length
        if abs(self.looper1.speed) > 10:
            # flip direction of speed increase
            self.speed_increment *= -1
        self.looper1.speed += self.speed_increment
        self.looper1.length = abs(int(round(self.looper1.speed))) + 1
