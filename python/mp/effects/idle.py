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
            'left_nail': self.left_hijack,
            'right_nail': self.right_hijack
        }
        # The base Effect class will check self.trigger_hijacks and
        # modify the rosary's behavior
        self.hijack_triggers()


    def left_hijack(self, *args):
        print("idle: left_hijack", *args)

    def right_hijack(self, *args):
        print("right_hijack", *args)


    def next(self):
        self.bin.next()


