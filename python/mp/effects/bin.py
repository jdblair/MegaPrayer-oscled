import copy
from mp import color
from mp.effects import effect

class Bin(effect.Effect):
    """
    """

    # Wish there were a better way than requiring this every time
    dm = copy.deepcopy(effect.Effect.dm)

    def __init__(self, bead_set, **kwargs):
        super().__init__(name="bin", **kwargs)
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
        effect.rosary = self.rosary
        self.effects.append(effect)

        #print("id", effect.id)

        return effect.id


#    @dm.expose()
    def del_effect(self, id):
        """Delete an active effect by id."""

        effect = self.effect(id)

        if effect is not None:
            #effect_paths = [effect.generate_osc_path(fn) for fn in\
            #                effect.dm.registered_methods.keys()]
            #self.effect_paths_to_unregister.extend(effect_paths)
            self.unexpose_effect_knobs(effect)
            self.effects.remove(effect)


#    @dm.expose()
    def clear_effects(self):
        """Remove all active effects. This stops all activity on the rosary."""
        # There's some weird race condition where del_effect's call to
        # self.effects.remove doesn't reorder the list in time if we use
        # a for loop, so do this instead
        while self.effects:
            effect = self.effects[0]
            self.del_effect(effect.id)

        # I know on the real rosary this is unneccessary, but it's
        # annoying on the sim: @jdblair is sending 0,0,0 in the real
        # thing wonky?
        self.add_effect('set_color', 'all', 0, 0, 0)


#    @dm.expose()
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
            #self.expose_effect_knobs(effect)

            effect.supernext()
            if (effect.finished):
                self.del_effect(effect.id)
