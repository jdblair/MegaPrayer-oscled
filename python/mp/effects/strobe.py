import copy
from mp import color
from mp.effects import effect

class Strobe(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="strobe", bead_set=bead_set, color=color, **kwargs)
        self.count = 0

    def next(self):
        if self.count == 27:
            for bead in self.bead_list:
                bead.color.set(self.color)
        if self.count > 29:
            for bead in self.bead_list:
                bead.color.set(self.color)
            self.count = 0
        self.count += 1
