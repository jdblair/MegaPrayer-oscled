import copy
from mp import color as _color
from mp.effects import effect, bin, fire_spreading

class BurnItAll(effect.Effect):
    """
    Just burn it tall. Burn it all down.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), **kwargs):
        super().__init__(name="burn_it_all", bead_set=bead_set, color=color, **kwargs)

        self.bin = bin.Bin(bead_set, rosary=self.rosary)

        self.cross_fire = fire_spreading.FireSpreading(bead_set=self.rosary.\
                                                       set_registry['cross'],
                                                       speed=.05,
                                                       initial_fires=3,
                                                       rosary=self.rosary)
        self.rosary_fire = fire_spreading.FireSpreading(bead_set=self.rosary.\
                                                        set_registry['rosary'],
                                                        speed=.005,
                                                        initial_fires=1,
                                                        rosary=self.rosary)
        self.base_fire = fire_spreading.FireSpreading(bead_set=self.rosary.\
                                                      set_registry['base'],
                                                      speed=.0002,
                                                      initial_fires=1,
                                                      rosary=self.rosary)

        self.bin.add_effect_object(self.cross_fire)
        self.bin.add_effect_object(self.rosary_fire)
        self.bin.add_effect_object(self.base_fire)

    def next(self):
        self.bin.next()
