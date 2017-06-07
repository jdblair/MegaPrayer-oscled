import copy
from mp import color
from mp.effects import effect

class Casino(effect.Effect):
    """
    Bounce colors a single bead, one at a time, from the lowest bead to
    the highest bead. Leave the highest bead lit until all the empty beads are full.
    Once all the beads are full, shut off all the beads simultaneously.

    self.direction is a positive or negative integer.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), duration=None, direction=1):
        super().__init__("casino", bead_set, color=color, duration=duration)
        self.direction = direction
        if (self.direction < 0):
            self.current = len(self.bead_list) - 1
        else:
            self.current = 0
        #self.last = self.current
        self.end_position = len(self.bead_list) - 1
        

    def next(self, rosary):
        super().next()

        #turn on all beads from end_position to end of bead set
        for b in range(self.end_position, len(self.bead_list)):
            self.bead_list[b].color.set(self.color)
        
        #self.bead_list[self.last].color.set(rosary.bgcolor)
        self.current += self.direction
        #self.last = self.current
        self.bead_list[self.current].color.set(self.color)

        if (self.current >= self.end_position):
            self.current = 0
            #self.last = 0
            self.end_position = self.end_position - 1
        if (self.end_position <= 0):
            #shut off all the beads and start over
            for b in self.bead_list:
                b.color.set(rosary.bgcolor)
            self.end_position = len(self.bead_list) - 1
            self.current = 0
            #self.last = 0


    @dm.expose()
    def set_direction(self, direction):
        self.direction = direction
