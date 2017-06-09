from mp.effects import bounce
from mp.triggers import trigger
from mp import color

class Test(trigger.Trigger):
    """
    I'll replace this with more useful documentation
    when I'm done patting myself on the back
    """

    def __init__(self):
        super().__init__("test")

    def inner_fire(self):
    
        bs = self.rosary.set_registry.get('all')
        col = color.Color(0.3, 0.6, 0.9)
        eff = bounce.Bounce(bead_set=bs, color=col)
        eff.delay=60
        eff.fade_out(120.0)

        self.rosary.add_effect_object(eff)
