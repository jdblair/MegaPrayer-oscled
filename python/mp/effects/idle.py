import copy
import time
from mp import color as _color
from mp.effects import effect, bin, shooter, set_color, level


class Idle(effect.Effect):
    """
    This effect will run when no other effect is running on the system.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(1.0, 1.0, 1.0), **kwargs):
        super().__init__(name="idle", bead_set=bead_set, color=color, **kwargs)

        self.color = color
        self.bin = bin.Bin(bead_set, rosary=self.rosary)

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
        
        # left and right nail flags
        self.left_nail_isset = False
        self.right_nail_isset = False
        # left and right nail timers
        self.left_nail_timer = time.time()
        self.right_nail_timer = time.time()

        self.left_nail_effect = None
        self.right_nail_effect = None
        
        # set an event timer to see when the last event occurred
        self.last_event = time.time()
    

            
    def left_nail(self, v):
        if (v == 1.0):
            if (self.left_nail_effect == None):
                self.left_nail_effect = level.Level(self.rosary.set_registry['half01'].union(self.rosary.set_registry['stem']), bead_set_sort='cw', color=self.color)
                self.bin.add_effect_object(self.left_nail_effect)
                
            self.left_nail_isset = True

        else:
            # no action
            self.left_nail_isset = False
            pass

    def right_nail(self, v):
        if (v == 1.0):
            if (self.right_nail_effect == None):
                self.right_nail_effect = level.Level(self.rosary.set_registry['half23'].union(self.rosary.set_registry['stem']), bead_set_sort='ccw', color=self.color)
                self.bin.add_effect_object(self.right_nail_effect)
                
            self.right_nail_isset = True

        else:
            # no action
            self.right_nail_isset = False
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
            if self.bead_effect[bead.index] == None:
                self.bead_effect[bead.index] = set_color.SetColor(frozenset([bead]), color=self.color)
                self.bin.add_effect_object(self.bead_effect[bead.index])
        else:
            if self.bead_effect[bead.index] != None:
                self.bead_effect[bead.index].fade_out(30)
                self.bead_effect[bead.index] = None
            

    def next(self):
        self.bin.next()
        if self.last_event <= time.time() - 15:
            # play a playlist of effects
            print("going idle; playing effects now")

        if (time.time() >= self.left_nail_timer and time.time() >= self.right_nail_timer):
            # kick the levels
            if (self.left_nail_isset == True):
                self.left_nail_effect.kick()
            if (self.right_nail_isset == True):
                self.right_nail_effect.kick()

            # are both nails at max_level?
            if ((self.left_nail_effect != None and self.left_nail_effect.level >= self.left_nail_effect.max_level) and
                (self.right_nail_effect != None and self.right_nail_effect.level >= self.right_nail_effect.max_level)):
                #turn on the spotlights and the music
                print("hallelujah!")
                # set an end time one minute from now
                self.left_nail_timer = time.time() + 60
                self.right_nail_timer = time.time() + 60

            if (self.left_nail_effect != None):
                if (self.left_nail_effect.level == 0):
                    self.bin.del_effect(self.left_nail_effect.id)
                    self.left_nail_effect = None

            if (self.right_nail_effect != None):                    
                if (self.right_nail_effect.level == 0):
                    self.bin.del_effect(self.right_nail_effect.id)
                    self.right_nail_effect = None

                    
        else:
        #     # no action until timer runs out (to prevent too many messiahs)
            pass
