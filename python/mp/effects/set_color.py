import copy
from mp.effects import effect
from mp import color

class SetColor(effect.Effect):
    """
    SetColor is a one-shot effect that sets all beads in a set to a given color.
    It removes itself from the mainloop after one invocation of next()
    """

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="set_color", bead_set=bead_set, color=color, **kwargs)

    def next(self):
        for bead in (self.bead_list):
            bead.color.set(self.color)


class SetColorUnique(effect.Effect):
    """
    Similar to SetColor, but each bead gets its own instance of the color object.

    This is for dynamic colors so that each bead will act similarly, but not identically.
    """

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="set_color_unique", bead_set=bead_set, color=color, **kwargs)

        # Give each bead its own copy of the color
        self.bead_colors = [copy.copy(color) for b in bead_set]

    def next(self):
        for bead, col in zip((self.bead_list), self.bead_colors):

            # effect.Effect's supernext(), which calls effect(), acts
            # directly on self.color, which isn't being used here.
            # Instead, we have to step the color
            col.next()
            bead.color.set(col)
