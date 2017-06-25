import copy
from mp.effects import effect
from mp import color

class Wheel(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=color.Color(), speed=0.5, length=3, start_offset=0, colors=[color.Color(0,0,0), color.Color(1,1,1)], **kwargs):
        super().__init__(name="wheel", bead_set=bead_set, color=color, **kwargs)
        self.current = start_offset
        self.speed = speed
        self.length = length
        self.colors = colors

        # make sure we don't exceed our limits
        if self.current > len(self.bead_list):
            self.current = len(self.bead_list)
        if self.length > len(self.bead_list):
            self.length = len(self.bead_list)

    def next(self):
        offset = int(round(self.current))
        color_i = 0
        color_length = 0
        for i in range(0,len(self.bead_list)):
            #print(i, color_i, color_length)
            self.bead_list[(offset + i) % len(self.bead_list)].color.set(self.colors[color_i])
            color_length += 1
            if color_length >= self.length:
                color_length = 0
                color_i += 1
                if color_i >= len(self.colors):
                    color_i = 0

        self.current += self.speed
        self.current = self.current % len(self.bead_list)

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed

    @dm.expose()
    def set_length(self, length):
        self.length = length

