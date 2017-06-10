
class EffectList:

    def __init__(self, rosary, parent_id=None):
        self.effects = []
        self.parent_id = parent_id
        self.effect_id_num = 0
        # we need to know about the rosary so we can set effect.rosary in add_effect_object()
        self.rosary = rosary

    def effect(self, id):
        """Return the Effect object of an active effect by specifying the Effect id."""
        for e in self.effects:
            if e.id == id:
                return e
        return None

    def effect_id(self):
        print("parent_id", self.parent_id)

        if self.parent_id == None:
            effect_id = str(self.effect_id_num)
        else:
            effect_id = str("{}.{}".format(self.parent_id, self.effect_id_num))

        self.effect_id_num += 1
        return effect_id

    def add_effect_object(self, effect):
        """Adds an Effect object to the active Effect list.  Returns the id of
        the active effect.

        """
        effect.id = self.effect_id()
        # Since rosary holds the dispatcher and the effect doesn't
        # know about rosary on init, we can't map to dispatcher yet either
        effect.rosary = self.rosary
        self.effects.append(effect)

        print("id", effect.id)

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

            #print("EffectList.next(): ", effect)

            # If any new effects have been added since the last iteration,
            # add their knobs to the dispatched functikon
            #self.expose_effect_knobs(effect)

            effect.supernext()
            if (effect.finished):
                self.del_effect(effect.id)

