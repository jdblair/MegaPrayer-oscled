import copy
import math

from mp import color
from mp.effects import effect

class Soft_Edges_Glow(effect.Effect):
    """
    Fade out the edges of a bead set gradually.

    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), **kwargs):
        super().__init__(name="soft_edges_glow", bead_set=bead_set, color=color, **kwargs)

    def next(self):
        for bead in (self.bead_list):
            bead.color.set(self.color)

        fade_beads = int(round(len(self.bead_list) / 3))
        fade_in = fade_beads
        fade_out = len(self.bead_list) - fade_beads


        r = self.color.r
        g = self.color.g
        b = self.color.b
        a = self.color.a

        
        r_delta = r / fade_beads
        g_delta = g / fade_beads
        b_delta = b / fade_beads
        #a_delta = a / fade_beads

        
        # fade out the colour towards the end of the bead_set
        for bead in (self.bead_list[fade_out:]):
            r = r - r_delta
            g = g - g_delta
            b = b - b_delta
            #a = a - a_delta

            bead.color.set(color.Color(r, g, b, a))


        r = int(self.rosary.bgcolor.r)
        g = int(self.rosary.bgcolor.g)
        b = int(self.rosary.bgcolor.b)
        a = int(self.rosary.bgcolor.a)

        # fade in the colour from the beginning of the bead_set
        for bead in (self.bead_list[:fade_in]):
            r = r + r_delta
            g = g + g_delta
            b = b + b_delta
            #a = a_bg = a_delta

            
            #fade in the colour
            bead.color.set(color.Color(r, g, b, a))


