import copy
from mp.effects import effect
from mp import color

class Level(effect.Effect):
    """
    The idea of Level is to show a bar-graph-style "level." The level increases when
    we receive a "kick." The level also decays naturally over time.

    The use case is that we want lights to "grow" out the stem and around the rosary
    when someone touches a nail.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="level", bead_set=bead_set, color=color, **kwargs)

        self.level = 0
        self.max_level = len(self.bead_list)

        self.kick_up = 3
        self.kick_down = 0.4

    def next(self):
        for i in range(0,int(round(self.level))):
            self.bead_list[i].color.set(self.color)
        self.level = self.level - self.kick_down
        self.level = max( self.level, 0 )

    @dm.expose()
    def kick(self):
        self.level = self.level + self.kick_up
        self.level = min(self.level, self.max_level)
        print('level', self.level)

