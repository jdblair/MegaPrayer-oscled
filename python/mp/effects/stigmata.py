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

    def __init__(self, bead_set, color=_color.Color(), **kwargs):
        super().__init__(name="stigmata", bead_set=bead_set, color=color, **kwargs)

        self.count = 0
        self.bin = bin.Bin(bead_set, rosary=self.rosary)

        self.bin.add_effect_object(
            soft_edges_glow.Soft_Edges_Glow(
                self.rosary.set_registry['stigmata_left'],
                self.rosary.color_registry['red']))

        self.bin.add_effect_object(
            soft_edges_glow.Soft_Edges_Glow(
                self.rosary.set_registry['stigmata_right'],
                self.rosary.color_registry['red']))

        self.bin.add_effect_object(
            soft_edges_glow.Soft_Edges_Glow(
                self.rosary.set_registry['stigmata_crown'],
                self.rosary.color_registry['yellow']))

        self.bin.add_effect_object(
            soft_edges_glow.Soft_Edges_Glow(
                self.rosary.set_registry['stigmata_left_foot'],
                self.rosary.color_registry['red']))

        self.bin.add_effect_object(
            soft_edges_glow.Soft_Edges_Glow(
                self.rosary.set_registry['stigmata_right_foot'],
                self.rosary.color_registry['red']))

    def next(self):
        self.bin.next()
