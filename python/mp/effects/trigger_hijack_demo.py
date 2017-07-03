import copy
from mp import color as _color
from mp.effects import effect, bin, looper, set_color

# The bead numbers that represent the hijacked triggers
LEFT_HIJACK = 7
RIGHT_HIJACK = 22

class TriggerHijack(effect.Effect):
    """
    Demo to show how to take over existing triggers from within an effect.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def left_hijack(self):
        print("Left nail hijack: BEAD #{}".format(self.red_looper.current))
        # I dunno, some black magic: https://stackoverflow.com/a/18994210
        if self.red_looper.current >= LEFT_HIJACK - 1 and \
           self.red_looper.current <= LEFT_HIJACK + 1:

            self.red_looper.set_speed(-1)

    def right_hijack(self):
        print("Right nail hijack: BEAD #{}".format(self.red_looper.current))
        if self.red_looper.current >= RIGHT_HIJACK - 1 and \
           self.red_looper.current <= RIGHT_HIJACK + 1:

            self.red_looper.set_speed(1)

    # If this effect is running and one of these triggers is fired,
    # execute associated method instead of what trigger would ordinarily do
    trigger_hijacks = {
        'left_nail': left_hijack,
        'right_nail': right_hijack
    }

    def __init__(self, bead_set, color=_color.Color(), **kwargs):
        bead_set = kwargs.get('rosary').set_registry['ring']
        super().__init__(name="trigger_hijack", bead_set=bead_set, color=color, **kwargs)

        # This effect uses 2 separate effects, so let's copy bin_demo.py
        self.bin = bin.Bin(bead_set, rosary=self.rosary)

        # If this were a game, this would be "the ball"
        self.red_looper = looper.Looper(bead_set=bead_set,
                                        color=_color.Color(1, 0, 0),
                                        **kwargs)
        self.bin.add_effect_object(self.red_looper)

        # Specifically, if this were pong, these might be the "paddles"
        self.hijacked_beads = set_color.SetColor(bead_set=frozenset([self.rosary.beads[11], self.rosary.beads[25]]), color=_color.Color(1,1,1), **kwargs)
        self.bin.add_effect_object(self.hijacked_beads)

        for k, v in self.trigger_hijacks.items():
            print("Hijacking rosary trigger {} with method {}".format(k, v))
            self.rosary.trigger_hijacks.setdefault(k, []).append((self,v))

    def next(self):
        self.bin.next()
