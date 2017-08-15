import copy
from mp import color as _color
from mp.effects import effect, bin, set_color, sine_wave, sparkle, firework
import random

class America(effect.Effect):
    """
    OH SAY CAN YOU SEE
    """

    # BY THE DAWN'S EARLY LIGHT
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), **kwargs):
        super().__init__(name="america", bead_set=bead_set, color=color, **kwargs)

        # WHAT SO PROUDLY WE HAILED
        self.bin = bin.Bin(bead_set=self.rosary.set_registry['cross'],
                           rosary=self.rosary)

        # AT THE TWILIGHT'S LAST GLEAMING
        self.red_base = set_color.SetColor(bead_set=self.rosary.\
                                                    set_registry['cross'],
                                           color=_color.Color(1, 0, 0))
        # WHOSE BROAD STRIPES AND BRIGHT STARS
        self.white_stripes = sine_wave.SineWave(bead_set=self.rosary.\
                                                         set_registry['cross'],
                                                color=_color.Color(1, 1, 1),
                                                period=16)
        # THROUGH THE PERILOUS FIGHT
        self.blue = set_color.SetColor(bead_set=self.rosary.\
                                                set_registry['stigmata_crown'],
                                       color=_color.Color(0, 0, 1))
        # O'ER THE RAMPARTS WE WATCHED
        self.stars = sparkle.Sparkle(bead_set=self.rosary.\
                                              set_registry['stigmata_crown'],
                                     color=_color.Color(1, 1, 1),
                                     size=10,
                                     speed=5)

        # WERE SO GALLANTLY STREAMING
        self.balls = set_color.SetColor(bead_set=self.rosary.\
                                                 set_registry['rosary'],
                                        color=_color.Color(.83, .68, .21))
        # AND THE ROCKETS RED GLARE
        self.ball_sparkle = sparkle.Sparkle(bead_set=self.rosary.\
                                                     set_registry['rosary'],
                                            color=_color.Color(1, 1, 0),
                                            size=3,
                                            speed=2)

        # THE BOMBS BURSTING IN AIR
        self.bases = set_color.SetColor(bead_set=self.rosary.\
                                                 set_registry['base'],
                                        color=_color.Color(.83, .68, .21))
        # GAVE PROOF THROUGH THE NIGHT
        self.base_sparkle = sparkle.Sparkle(bead_set=self.rosary.\
                                                     set_registry['base'],
                                            color=_color.Color(1, 1, 0),
                                            size=1,
                                            speed=5)

        # THAT OUR FLAG WAS STILL THERE
        self.bin.add_effect_object(self.red_base)
        self.bin.add_effect_object(self.white_stripes)
        self.bin.add_effect_object(self.blue)
        self.bin.add_effect_object(self.stars)

        # OH SAY DOES THAT STAR-SPANGLED BANNER YET WAVE
        self.bin.add_effect_object(self.balls)
        self.bin.add_effect_object(self.ball_sparkle)

        # O'ER THE LAND OF THE FREE
        self.bin.add_effect_object(self.bases)
        self.bin.add_effect_object(self.base_sparkle)

    # AND THE HOME OF THE BRAVE
    def next(self):
        self.bin.next()

        # I RAN OUT OF LYRICS, BUT HOW 'BOUT SOME FIREWORKS
        if random.random() > .99:

            if random.random() > .5:
                direction = "cw"
            else:
                direction = "ccw"

            firework_color = random.choice([
                                _color.Color(1, 0, 0, .7),
                                _color.Color(1, 1, 1, .7),
                                _color.Color(0, 0, 1, .7)
                             ])

            fw = firework.Firework(bead_set=self.rosary.\
                                            set_registry['rosary'],
                                   color=firework_color,
                                   rosary=self.rosary,
                                   direction=direction)
            self.bin.add_effect_object(fw)
