import copy
from mp import color as _color
from mp.effects import effect, bin, soft_edges_glow

class Stigmata(effect.Effect):
    """
    The Stigmata, to be used with the Cross bead set.
    Makes the crown, hands, and feet of the cross glow
    with a fade

    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, **kwargs):
        super().__init__(name="stigmata", bead_set=bead_set, color=color, **kwargs)

        self.count = 0
        self.bin = bin.Bin(bead_set, rosary=self.rosary)

        #self.bin.add_effect_object(soft_edges_glow.Soft_Edges_Glow(bead_set='stigmata_left', color=_color.Color(0, 1, 0)))
        self.bin.add_effect_object(name='soft_edges_glow', bead_set='stigmata_right', color=_color.Color(0, 1, 0))
        #self.bin.add_effect_object(name='soft_edges_glow', color='yellow', bead_set='stigmata_crown')
        #self.bin.add_effect_object(name='soft_edges_glow', color='red', bead_set='stigmata_left_foot')
        #self.bin.add_effect_object(name='soft_edges_glow', color='red', bead_set='stigmata_right_foot')


    def next(self):
        self.bin.next()
