from collections import namedtuple
import random


class Color:
    """Color represents the color of an individual bead."""
    
    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0, name='color'):
        self.r = r  # red
        self.g = g  # green
        self.b = b  # blue
        self.a = a  # alpha channel (not yet used)
        self.brightness = 0xff;  # brightness used by APA102 LED module
        self.name = name

    def __repr__(self):
        return "Color({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)

    def _set(self, color, intensity=1):
        """copy the r, g, b and a values into a Color object.
        intensity is an optional argument."""
        self.r = color.r * intensity
        self.g = color.g * intensity
        self.b = color.b * intensity
        self.a = color.a

    def set(self, color, intensity=1, alpha=None):
        """blend the r, g, b and a values in a Color object,
        using the Porter and Duff equation for alpha blending
        intensity is an optional argument."""

        if alpha == None:
            # take alpha from supplied color object
            alpha = color.a

        # this part is the porter-duff equation
        self.a = max(1, alpha + (self.a * (1 - alpha)))
        if self.a == 0:
            self.r = 0
            self.g = 0
            self.b = 0
        else:
            self.r = (((color.r * alpha) + (self.r * (1 - alpha))) / self.a) * intensity
            self.g = (((color.g * alpha) + (self.g * (1 - alpha))) / self.a) * intensity
            self.b = (((color.b * alpha) + (self.b * (1 - alpha))) / self.a) * intensity

        self.a = alpha

    def next(self):
        """No-op in most cases. This is used by child objects that implement
        dynamic color features."""
        pass



ColorMapStep = namedtuple('ColorMapStep', 'step color')


class ColorMap(Color):
    """
    ColorMap is a special case of Color() that defines a linear color map, mapping a range to a color.
    By convention I expect we will use the range (0,1) but any range is actually possible.

    The map is defined as a list of ColorMapStep, which maps a value to a color.
    If the value we map is between two ColorMapStep the linear interpolation is calculated.

    The ColorMap is a Color object - you can set r, g, b and a just like any other Color object.
    However, it is intended that the color is set using map(), which maps a value in the
    defined range to a color.

    e.g.:
    # default color map is black to 100% white
    cm = ColorMap()
    # set bead.color to 43% gray
    bead.color.set(cm.map(0.43))

    Example colormap covering all possible RGB colors, with both 0 and 1 set to 100% blue:
    [
      ColorMapStep(step=0,   color=Color(1, 0, 0)),
      ColorMapStep(step=1/3, color=Color(0, 1, 0)),
      ColorMapStep(step=2/3, color=Color(0, 0, 1)),
      ColorMapStep(step=1,   color=Color(1, 0, 0))
    ]                                                                           

    Alpha channel can also be defined in the colormap.
    For example, to map a range from 100% transparent to 100% opaque, do this:
    [
      ColorMapStep(step=0, color=Color(0, 0, 0, 0)),
      ColorMapStep(step=1, color=Color(0, 0, 0, 1))
    ]
    """

    def __init__(self, colormap=[ColorMapStep(0, Color(0, 0, 0)), ColorMapStep(1, Color(1, 1, 1))]):
        super().__init__(r=colormap[0].color.r, g=colormap[0].color.g, b=colormap[0].color.b, a=colormap[0].color.a, name='color_map')
        self.colormap = colormap

    def __repr__(self):
        return "ColorMap(r={}, g={}, b={}, a={}, colormap={})".format(self.r, self.g, self.b, self.a, self.colormap)


    def map(self, value):

        def interpolate(x0, y0, x1, y1, xv):
            if (y0 == y1):
                return y0

            return y0 + (( (y1 - y0) / (x1 - x0) ) * (xv - x0))

        # first check lower bound
        if (value <= self.colormap[0].step):
            self.set(self.colormap[0].color)
            return

        # then upper bound
        if (value >= self.colormap[-1].step):
            self.set(self.colormap[-1].color)
            return

        # now search for steps to interpolate color between
        m0 = self.colormap[0]
        for m1 in self.colormap[1:]:
            # check easy case before doing math
            if (value == m1.step):
                self.set(m1.color)
                return

            if (value < m1.step):
                # interpolate color
                self.r = interpolate(m0.step, m0.color.r, m1.step, m1.color.r, value)
                self.g = interpolate(m0.step, m0.color.g, m1.step, m1.color.g, value)
                self.b = interpolate(m0.step, m0.color.b, m1.step, m1.color.b, value)
                self.a = interpolate(m0.step, m0.color.a, m1.step, m1.color.a, value)
                return

            m0 = m1


class ColorMapFade(Color):
    """
    ColorMapFade() is a dynamic Color() which cycles through a provided ColorMap() over time steps.
    """
    def __init__(self, colormap=ColorMap(colormap=[ColorMapStep(0, Color(0, 0, 0)), ColorMapStep(1, Color(1, 1, 1))]), time=30, name='color_map_fade'):
        super().__init__(r=colormap.colormap[0].color.r,
                         g=colormap.colormap[0].color.g,
                         b=colormap.colormap[0].color.b,
                         a=colormap.colormap[0].color.a, name=name)
        self.colormap = colormap
        self.delta = 0
        self.time = time
        self.delta_t = 1 / time
        print("NEW COLOR MAP FADE")
        print(self.colormap)

    def __repr__(self):
        return "ColorMap(r={}, g={}, b={}, a={}, colormap={}, time={})".format(self.r, self.g, self.b, self.a, self.colormap, self.time)

    def next(self):
        self.delta += self.delta_t
        self.colormap.map(self.delta)
        print("DELTA IS {}".format(self.delta))
        self.set(self.colormap)
        if (self.delta >= 1) or (self.delta <= 0):
            self.delta_t *= -1


class ColorMapRandomWalk(Color):
    """
    Instead of smoothly fading across the Colors in a ColorMap, randomly walk within the values.
    """
    def __init__(self, colormap=ColorMap(colormap=[ColorMapStep(0, Color(0, 0, 0)), ColorMapStep(1, Color(1, 1, 1))]), time=30, name='color_map_fade'):
        super().__init__(r=colormap.colormap[0].color.r,
                         g=colormap.colormap[0].color.g,
                         b=colormap.colormap[0].color.b,
                         a=colormap.colormap[0].color.a, name=name)
        self.colormap = colormap
        self.delta = 0
        self.time = time
        self.delta_t = 1 / time

    def __repr__(self):
        return "ColorMap(r={}, g={}, b={}, a={}, colormap={}, time={})".format(self.r, self.g, self.b, self.a, self.colormap, self.time)

    def next(self):
        self.delta += self.delta_t
        self.colormap.map(self.delta)
        self.set(self.colormap)

        breakpoints = [c[0] for c in self.colormap.colormap]
        breakpoints.remove(0)
        breakpoints.remove(1)

        if (self.delta >= 1) or (self.delta <= 0):
            print("BOUNDARIES")
            self.delta_t *= -1

        #elif any(self.delta + self.delta_t > b and self.delta < b for b in breakpoints):
        elif any(self.delta - self.delta_t < b and self.delta > b for b in breakpoints):
            print("BREAK!")
            print(breakpoints)
            print(self.delta, self.delta_t, self.delta+self.delta_t)
            if random.random() > .5:
                print("SWITCH!")
                self.delta_t *= -1


class ColorFade(ColorMapFade):
    """Represents a dynamic Color that fades linearly over time between to specificed colors.
    This is now implemented as a trivial case of ColorMapFade.

    knobs:
    time: number of steps to complete one color fade
    """

    def __init__(self, start=Color(0.0, 0.0, 0.0), finish=Color(1.0, 1.0, 1.0), time=30):
        super().__init__(colormap=ColorMap(colormap=[ColorMapStep(0, start), ColorMapStep(1, finish)]),
                         time=time,
                         name='color_fade')
        self.start = start
        self.finish = finish

    def __repr__(self):
        return "ColorFade(start={}, finish={}, time={})".format(self.start, self.finish, self.time)

    def next(self):
        super().next()


rainbow_map = [ColorMapStep(0, Color(1, 0, 0)), ColorMapStep(1/3, Color(0, 1, 0)), ColorMapStep(2/3, Color(0, 0, 1)), ColorMapStep(1, Color(1, 0, 0))]
