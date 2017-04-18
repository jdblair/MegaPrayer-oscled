from mp.effects import effect
from mp import color

class SetColor(Effect):
    """
    SetColor is a one-shot effect that sets all beads in a set to a given color.
    It removes itself from the mainloop after one invocation of next()
    """

    def __init__(self, bead_set, color=color.Color()):
        super().__init__("set_color", bead_set, color=color)

    def next(self, rosary):
        super().next()

        for bead in (self.bead_list):
            bead.copy_color(self.color)

        self.finished = True
