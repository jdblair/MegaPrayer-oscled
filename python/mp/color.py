class Color:
    """Represents individual Bead color data"""
    
    def __init__(self, r=0, g=0, b=0, a=0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
        return "Color({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)

    def set_intensity(self, intensity):
        self.r *= intensity
        self.g *= intensity
        self.b *= intensity
        
    def set(self, color, intensity=1):
        self.r = color.r * intensity
        self.g = color.g * intensity
        self.b = color.b * intensity
        self.a = color.a

    def next(self):
        pass

class ColorFade(Color):
    """Represents a dynamic Color that changes over time"""

    def __init__(self, start=Color(0,0,0), finish=Color(1,1,1), time=30):
        super().__init__(r=start.r, g=start.g, b=start.b, a=start.a)
        self.start = start
        self.finish = finish
        self.delta_t = time
        self.delta_r = (finish.r - start.r) / time
        self.delta_g = (finish.g - start.g) / time
        self.delta_b = (finish.b - start.b) / time

    def __repr__(self):
        return "ColorFade(start={}, finish={})".format(self.start, self.finish)

    def next(self):
        self.r += self.delta_r
        self.g += self.delta_g
        self.b += self.delta_b
        
        # correct for rounding errors that may cause us to exceed bounds
        if (self.r <= 0):
            self.r = 0
            self.delta_r *= -1
        if (self.r >= 1):
            self.r = 1
            self.delta_r *= -1
        if (self.g <= 0):
            self.g = 0
            self.delta_g *= -1
        if (self.g >= 1):
            self.g = 1
            self.delta_g *= -1
        if (self.b <= 0):
            self.b = 0
            self.delta_b *= -1
        if (self.b >= 1):
            self.b = 1
            self.delta_b *= -1
