import copy
from mp import color as _color
from mp.effects import effect, bin, shooter, set_color


class Idle(effect.Effect):
    """
    This effect will run when no other effect is running on the system.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(1.0, 1.0, 1.0), **kwargs):
        super().__init__(name="idle", bead_set=bead_set, color=color, **kwargs)

        self.bin = bin.Bin(bead_set, rosary=self.rosary)
        self.color = color

        # define the trigger functions
        self.trigger_hijacks = {
            'left_nail': self.left_nail,
            'right_nail': self.right_nail,
            'bead': self.bead_trigger
        }
        self.hijack_triggers()

        self.bead_effect = {}
        for b in self.bead_list:
            self.bead_effect[b.index] = None

            
    def left_nail(self, v):
        if (v == 1.0):
            self.left_nail_effect = shooter.Shooter(self.rosary.set_registry['half01'].union(self.rosary.set_registry['stem']), bead_set_sort='cw', color=self.color)
            self.bin.add_effect_object(self.left_nail_effect)
        else:
            # no action
            pass


    def right_nail(self, v):
        if (v == 1.0):
            self.right_nail_effect = shooter.Shooter(self.rosary.set_registry['half23'].union(self.rosary.set_registry['stem']), bead_set_sort='ccw', color=self.color)
            self.bin.add_effect_object(self.right_nail_effect)
        else:
            # no action
            pass


    def bead_trigger(self, v, number):
        # map the bead number to a bead (should there be a pre-populated dictionary to make this more efficient?)
        bead = None
        for b in self.bead_list:
            if b.index == number:
                bead = b
        if bead == None:
            return

        if (v == 1.0):
            self.bead_effect[bead.index] = set_color.SetColor(frozenset([bead]), color=self.color)
            self.bin.add_effect_object(self.bead_effect[bead.index])
        else:
            self.bead_effect[bead.index].fade_out(30)
            

    def next(self):
        self.bin.next()
