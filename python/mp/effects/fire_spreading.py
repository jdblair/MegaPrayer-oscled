import copy
from mp import color
from mp.effects import effect
import math, random

class FireSpreading(effect.Effect):
    """
    Spread fire

    knobs:
    * speed: How quickly the fire spreads, different for each bead set
             depending on how many beads are in the set

        cross: .05 seems reasonable
        rosary: .005 seems reasonable
        base: .0002 seems reasonable

    * initial_fires: How many random fires to start, much like speed

        cross: 3 seems reasonable
        rosary: 1 seems reasonable
        base: 1 seems reasonable
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)
    
    def __init__(self, bead_set, color=color.Color(), speed=.1, initial_fires=1, **kwargs):
        super().__init__(name="fire_spreading", bead_set=bead_set, color=color, **kwargs)

        # I'm too scared to just remove the color arg, but in actuality
        # I'm going to ignore whatever you pass and just set all beads
        # to the same instance of the "fire" color
        if self.rosary is not None:
            self.color = self.rosary.color_registry['fire']

        # NOTE: Speed here should definiltey be 0 < n < 1
        # Even at speed 1, a bead's neighbours are 94% likely to be on fire
        # after only 10 cycles (that's too fast!)
        self.speed = speed

        # Keep a mapping of how long each bead has been "on fire"
        self.on_fire_cycles = {}

        # To start, randomly light a bead on fire
        # NOTE: During effect registration we get init'd with no bead_list
        if len(self.bead_list) > 0:

            for i in range(initial_fires):
                some_bead_index = random.randrange(len(self.bead_list))
                self.on_fire_cycles[some_bead_index] = 1

    def next(self):

        # For every bead that is on fire, check if we should light our
        # neighbours on fire too
        for bead_index in range( len(self.bead_list) ):

            on_fire = self.on_fire_cycles.get(bead_index)

            if on_fire is not None:

                # First, if this bead is on fire, color it so
                self.bead_list[bead_index].color.set(self.color)

                # The longer this bead has been "on fire", the more likely
                # it is to light its neighbours on fire
                # Conveniently, arctan has an astymptote at pi/2
                ignition_probability = math.atan(self.speed * on_fire) / (math.pi/2)

                for neighbour_index in (bead_index-1, bead_index+1):

                    # If neighbour_index == -1, it'll wrap around nicely, but
                    # if neighbour_index == len(self.bead_list), manually set
                    # to be 0 instead
                    if neighbour_index > len(self.bead_list)-1:
                        neighbour_index = 0

                    # As ignition_probability grows over time, we want more
                    # rolls of random.random() to fall within it
                    if self.on_fire_cycles.get(neighbour_index, 0) <= 0:
                        if random.random() < ignition_probability:
                            self.on_fire_cycles[neighbour_index] = 1

                self.on_fire_cycles[bead_index] += 1

        

    @dm.expose()
    def set_speed(self, speed):
        self.speed = speed
