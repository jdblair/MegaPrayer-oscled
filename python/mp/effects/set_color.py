
from mp.effects import effect
from mp import color

class SetColor(effect.Effect):
    """
    SetColor sets all beads in a set to a given color.
    """

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="set_color", bead_set=bead_set, color=color, **kwargs)

    def next(self):
        for bead in (self.bead_list):
            bead.color.set(self.color)
