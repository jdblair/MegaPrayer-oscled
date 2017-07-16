import copy
from mp import color as _color
from mp.effects import effect, bin, looper, set_color


class Idle(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), **kwargs):
        bead_set = kwargs.get('rosary').set_registry['ring']
        super().__init__(name="idle", bead_set=bead_set, color=color, **kwargs)

        # This effect uses 2 separate effects, so let's copy bin_demo.py
        self.bin = bin.Bin(bead_set, rosary=self.rosary)

        # NOTE: THIS IS THE MAIN ATTRACTION HERE!!!
        self.trigger_hijacks = {
            'left_nail': self.left_nail,
            'right_nail': self.right_nail,
            'bead00': self.bead00
        }
        # The base Effect class will check self.trigger_hijacks and
        # modify the rosary's behavior
        self.hijack_triggers()


    def left_nail(self, *args, **kwargs):
        print("idle: left_hijack", *args, **kwargs)

    def right_nail(self, *args, **kwargs):
        print("right_hijack", *args, **kwargs)

    def bead00(self, *args, **kwargs):
        print("bead00", *args, **kwargs)


    def next(self):
        self.bin.next()


