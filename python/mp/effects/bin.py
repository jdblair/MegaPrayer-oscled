import copy
from mp import color
from mp.effects import effect

class Bin(effect.Effect):
    """
    This effect contains a list of other effects. Calling next() invokes the next() method
    on all the contained effects. Rosary actually only contains this one effect, adding and
    removing effects to and from it.

    In other words, its turtles all the way down.
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, **kwargs):
        super().__init__(name="bin", bead_set=bead_set, **kwargs)
        self.effects = []
        self.effect_id_num = 0

    def effect(self, id):
        """Return the Effect object of an active effect by specifying the Effect id."""
        for e in self.effects:
            if e.id == id:
                return e
        return None    

    def effect_id(self):
        self.effect_id_num += 1
        return self.effect_id_num

    def add_effect_object(self, effect):
        """Adds an Effect object to the active Effect list.  Returns the id of
        the active effect.

        """
        effect.id = self.effect_id()
        # Since rosary holds the dispatcher and the effect doesn't
        # know about rosary on init, we can't map to dispatcher yet either
        self.effects.append(effect)
        effect.rosary = self.rosary

        return effect.id

    def set_rosary(self, rosary):
        """
        Make sure rosary is set in all contained effects.
        """
        for effect in self.effects:
            effect.set_rosary(rosary)
            super().set_rosary(rosary)

    def del_effect(self, id):
        """Delete an active effect by id."""
        effect = self.effect(id)

        if effect is not None:
            self.rosary.unexpose_effect_knobs(effect)

            # If this effect hijacked any triggers, time to un-hijack them
            # NOTE: Because this doesn't have that decorator fanciness,
            #       we can just call the method on the effect
            effect.unhijack_triggers()

            self.effects.remove(effect)

    def clear_effects(self):
        """Remove all active effects. This stops all activity on the rosary."""
        # There's some weird race condition where del_effect's call to
        # self.effects.remove doesn't reorder the list in time if we use
        # a for loop, so do this instead
        while self.effects:
            effect = self.effects[0]
            self.del_effect(effect.id)

    def clear_effects_fade(self):
        """
        Just calling clear_effects() is jarring, let's ease it in
        """

        for eff in self.effects:
            eff.fade_out(30)

    def next(self):
        for effect in self.effects:

            # If any new effects have been added since the last iteration,
            # add their knobs to the dispatched functikon
            self.rosary.expose_effect_knobs(effect)

            effect.supernext()

            if (effect.finished):
                self.del_effect(effect.id)
