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

    def __init__(self, bead_set, color=color.Color(), duration=None, speed=1, **kwargs):
        super().__init__(name="casino", bead_set=bead_set, color=color, duration=duration, **kwargs)

        self.set_speed(speed)

        if (self.speed < 0):
            self.current = len(self.bead_list) - 1
        else:
            self.current = 0
        self.end_position = len(self.bead_list) - 1
        

    def next(self):

        # turn on all beads from end_position to end of bead set
        for b in range(self.end_position, len(self.bead_list)):
            self.bead_list[b].color.set(self.color)
        
        self.current += int(round(self.speed))
        if (self.current > self.end_position):
            self.current = self.end_position
        
        # as the speed goes up we "stretch" the bead out
        for i in range(min(self.current,self.length)):
            self.bead_list[self.current - i].color.set(self.color)

        #print("self.current", self.current)
        
        if (self.current >= self.end_position):
            self.current = 0
            self.end_position = self.end_position - 1

        if (self.end_position <= 0):
            # shut off all the beads and start over
            for b in self.bead_list:
                b.color.set(self.rosary.bgcolor)
            self.end_position = len(self.bead_list) - 1
            self.current = 0


    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed
        self.length = abs(int(round(self.speed)))
        
        # don't let the length round down to zero
        if (self.length == 0):
            self.length = 1
