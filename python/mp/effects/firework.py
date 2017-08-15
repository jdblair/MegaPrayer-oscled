import copy
from mp import color as _color
from mp.effects import effect, bin, shooter, risefall
import math

class Firework(effect.Effect):
    """
    Random fill the cross, and have the rosary 
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), direction="ccw", **kwargs):
        super().__init__(name="firework", bead_set=bead_set, color=color, **kwargs)

        self.bin = bin.Bin(bead_set=self.rosary.set_registry['cross'],
                           rosary=self.rosary)

        self.fire = shooter.Shooter(bead_set=self.rosary.set_registry['rosary'],
                                    #color=_color.Color(1, 0, 0),
                                    color=color,
                                    speed=3,
                                    length=3,
                                    bead_set_sort=direction,
                                    parabolic=True)

        self.expl_left = risefall.RiseFall(bead_set=self.rosary.set_registry['cross_left_halfway_up'],
                                           delay=80,
                                           #color=_color.Color(1, 1, 0),
                                           color=color,
                                           speed=10,
                                           parabolic=True,
                                           once=True)

        self.expl_right = risefall.RiseFall(bead_set=self.rosary.set_registry['cross_right_halfway_up'],
                                           delay=80,
                                           #color=_color.Color(1, 1, 0),
                                           color=color,
                                           speed=10,
                                           parabolic=True,
                                           once=True,
                                           bead_set_sort='reverse')

        self.bin.add_effect_object(self.fire)
        self.bin.add_effect_object(self.expl_left)
        self.bin.add_effect_object(self.expl_right)

    def next(self):
        self.bin.next()
