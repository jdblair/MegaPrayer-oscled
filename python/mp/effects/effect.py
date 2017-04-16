from mp import color

class Effect:
    def __init__(self, name, set, color=color.Color(1,1,1)):
        self.name = name
        self.bead_set = self.set_bead_set(set)
        self.color = copy.copy(color)
        self.duration = 0
        self.id = -1
        self.finished = False # remove from effect list if true

    def __eq__(self, other):
        return (self.id == other)

    def __repr__(self):
        return "<Effect:{}: id={}>".format(self.name, self.id)
        
    """convenience function for converting sets to lists"""
    def set_bead_set(self, set):
        beads = []
        for bead in set:
            beads.append(bead)
        beads.sort(key=lambda bead: bead.index)
        self.bead_list = beads

    def get_name(self):
        return self.name

    def next(self):
        self.color.next()

class SetColor(Effect):
    def __init__(self, bead_set, color=color.Color()):
        super().__init__("set_color", bead_set, color=color)

    def next(self, rosary):
        super().next()

        for bead in (self.bead_list):
            bead.copy_color(self.color)

        self.finished = True
