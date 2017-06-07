class Color:
    """Color represents the color of an individual bead."""
    
    def __init__(self, r=0, g=0, b=0, a=0, name='color'):
        self.r = r  # red
        self.g = g  # green
        self.b = b  # blue
        self.a = a  # alpha channel (not yet used)

    def __repr__(self):
        return "Color({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)

    def _set(self, color, intensity=1):
        """copy the r, g, b and a values into a Color object.
        intensity is an optional argument."""
        self.r = color.r * intensity
        self.g = color.g * intensity
        self.b = color.b * intensity
        self.a = color.a

    def set(self, color, intensity=1):
        """blend the r, g, b and a values in a Color object,
        using the Porter and Duff equation for alpha blending
        intensity is an optional argument."""
        self.a = color.a + (self.a * (1 - color.a))
        if self.a == 0:
            self.r = 0
            self.g = 0
            self.b = 0
        else:
            self.r = (((color.r * color.a) + (self.r * (1 - color.a))) / self.a) * intensity
            self.g = (((color.g * color.a) + (self.g * (1 - color.a))) / self.a) * intensity
            self.b = (((color.b * color.a) + (self.b * (1 - color.a))) / self.a) * intensity

    def next(self):
        """No-op in most cases. This is used by child objects that implement
        dynamic color features."""
        pass


class ColorFade(Color):
    """Represents a dynamic Color that fades linearly over time between to specificed colors.

    knobs:
    time: number of steps to complete one color fade
    """

    def __init__(self, start=Color(0,0,0), finish=Color(1,1,1), time=30):
        super().__init__(r=start.r, g=start.g, b=start.b, a=start.a, name='color_fade')
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
