import copy
from mp import color as _color
from mp.effects import effect, bin, set_color, sine_wave, sparkle

class America(effect.Effect):
    """
    OH SAY CAN YOU SEE
    """

    # I WISH FOR NOTHING BECAUSE EVERYTHING IS AS IT SHOULD BE
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, color=_color.Color(), **kwargs):
        super().__init__(name="america", bead_set=bead_set, color=color, **kwargs)

        # IGNORE THE ARGS BECAUSE NOBODY TELLS US WHAT TO DO
        self.bin = bin.Bin(bead_set=self.rosary.set_registry['cross'],
                           rosary=self.rosary)

        # FIRST, START WITH A PATRIOTIC BASE
        self.red_base = set_color.SetColor(bead_set=self.rosary.\
                                                    set_registry['cross'],
                                           color=_color.Color(1, 0, 0))
        # ADD A LAYER OF PATRIOTIC STRIPES
        self.white_stripes = sine_wave.SineWave(bead_set=self.rosary.\
                                                         set_registry['cross'],
                                                color=_color.Color(1, 1, 1),
                                                period=16)
        # A NOBLE BLUE
        self.blue = set_color.SetColor(bead_set=self.rosary.\
                                                set_registry['stigmata_crown'],
                                       color=_color.Color(0, 0, 1))
        # A GLORIOUS SEA OF STARS
        self.stars = sparkle.Sparkle(bead_set=self.rosary.\
                                              set_registry['stigmata_crown'],
                                     color=_color.Color(1, 1, 1),
                                     size=10,
                                     speed=5)

        # HERE IN AMERICA WE HAVE BIG GOLD BALLS
        self.balls = set_color.SetColor(bead_set=self.rosary.\
                                                 set_registry['rosary'],
                                        color=_color.Color(.83, .68, .21))
        # THAT'S RIGHT MOTHERFUCKER, YOU REAAD THAT RIGHT
        # BALL SPARKLE
        self.ball_sparkle = sparkle.Sparkle(bead_set=self.rosary.\
                                                     set_registry['rosary'],
                                            color=_color.Color(1, 1, 0),
                                            size=3,
                                            speed=2)

        # YOU KNOW WHAT, JUST MAKE THE BASES GOLD TOO
        self.bases = set_color.SetColor(bead_set=self.rosary.\
                                                 set_registry['base'],
                                        color=_color.Color(.83, .68, .21))
        self.base_sparkle = sparkle.Sparkle(bead_set=self.rosary.\
                                                     set_registry['base'],
                                            color=_color.Color(1, 1, 0),
                                            size=1,
                                            speed=5)

        # ADD THAT SHIT IN
        self.bin.add_effect_object(self.red_base)
        self.bin.add_effect_object(self.white_stripes)
        self.bin.add_effect_object(self.blue)
        self.bin.add_effect_object(self.stars)

        self.bin.add_effect_object(self.balls)
        self.bin.add_effect_object(self.ball_sparkle)

        self.bin.add_effect_object(self.bases)
        self.bin.add_effect_object(self.base_sparkle)

    def next(self):
        self.bin.next()
