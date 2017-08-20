import copy
from mp import color as _color
from mp.effects import effect, bin, set_color

class Test(effect.Effect):
    """
    React to messages to test sets of LEDs
    """
    
    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)
    
    def __init__(self, bead_set, color=_color.Color(), **kwargs):
        super().__init__(name="test", bead_set=bead_set, color=color, **kwargs)

        self.bin = bin.Bin(bead_set, rosary=self.rosary)
        
        self.color = _color.Color(1, 1, 1)
        self.supply_effect = {}
        self.all_effect = None;
        self.cross_effect = {}
        self.spot_effect = {}
        
        # define the trigger functions
        self.trigger_hijacks = {
            'test_supply': self.test_supply,
            'test_color': self.test_color,
            'test_all': self.test_all,
            'test_cross': self.test_cross,
            'test_spots': self.test_spots
        }
        self.hijack_triggers()


    # set a color value
    def test_color(self, v, rgb):
        if (rgb == 'r'):
            self.color.r = v
        if (rgb == 'g'):
            self.color.g = v
        if (rgb =='b'):
            self.color.b = v

        for key in self.supply_effect.keys():
            if (self.supply_effect[key] != None):
                self.bin.effect(self.supply_effect[key]).color.set(self.color)

        for key in self.cross_effect.keys():
            if (self.cross_effect[key] != None):
                self.bin.effect(self.cross_effect[key]).color.set(self.color)

        if (self.all_effect != None):
                self.bin.effect(self.all_effect).color.set(self.color)

                
    # activate the color on a power supply
    def test_supply(self, v, x, y):
        """
        Turn on/off all the beads connected to a particular supply
        """

        # touchosc numbering is 1 indexed
        supply_beads = {
            1: frozenset(self.rosary.beads[0:10]),
            2: frozenset(self.rosary.beads[10:20]),
            3: frozenset(self.rosary.beads[20:30]),
            4: frozenset(self.rosary.beads[30:40]),
            5: frozenset(self.rosary.beads[40:50]),
            6: frozenset(self.rosary.beads[50:60])
        }

        if (v == 0):
            try:
                self.bin.del_effect(self.supply_effect[x])
            except KeyError:
                pass
            self.supply_effect[x] = None
        else:
            self.supply_effect[x] = self.bin.add_effect_object(set_color.SetColor(supply_beads[x], color=self.color))


    def test_all(self, v):
        """
        Turn on/off all the lights on the rosary.
        """
        if (v == 0):
            if (self.all_effect != None):
                self.bin.del_effect(self.all_effect)
            self.all_effect = None
        else:
            self.all_effect = self.bin.add_effect_object(set_color.SetColor(self.rosary.set_registry['all'], color=self.color))


    def test_spots(self, v, x, y):
        """
        Test the spots. The trigger is a 1 x 2 multitoggle.
        """

        print("test_spots", v, x, y)

        spot_beads = {
            1: self.rosary.set_registry['spot0'],
            2: self.rosary.set_registry['spot1']
        }

        if (v == 0):
            try:
                print("delete ", self.spot_effect[x])
                self.bin.del_effect(self.spot_effect[x])
            except KeyError:
                pass
            self.spot_effect[x] = None
        else:
            self.spot_effect[x] = self.bin.add_effect_object(set_color.SetColor(spot_beads[x], color=self.color))
            print("add effect", self.spot_effect[x])


    def test_cross(self, v, x, y):
        """
        Test the cross. The trigger is a 1 x 2 multitoggle.
        """
        cross_beads = {
            1: self.rosary.set_registry['cross_left'],
            2: self.rosary.set_registry['cross_right']
        }

        if (v == 0):
            try:
                self.bin.del_effect(self.cross_effect[x])
            except KeyError:
                pass
            self.cross_effect[x] = None
        else:
            self.cross_effect[x] = self.bin.add_effect_object(set_color.SetColor(cross_beads[x], color=self.color))


    def next(self):
        self.bin.next()

