import random
#from mp.effects import bounce, sine_wave
from mp.triggers import trigger

class LowPowerMode(trigger.Trigger):
    """
    Let something hit this trigger to signal whether we're in low power mode

    To go into low power mode:

        oscsend localhost 5006 /trigger/low_power_mode i 1

    To go into normal power mode:

        oscsend localhost 5006 /trigger/low_power_mode i 0
    """

    # Need to give it a default so it doesn't die on registration
    def __init__(self, enable_low_power_mode=False):
        super().__init__("low_power_mode")
        # Turn the int/float that we get into a bool
        self.low_power_mode = enable_low_power_mode > 0

    def inner_fire(self):
        self.rosary.low_power_mode = self.low_power_mode
