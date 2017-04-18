#!/usr/bin/python3
import argparse
from mp import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="OSC server address")
    parser.add_argument("--port", default=5005, help="OSC server port")
    args = parser.parse_args()

    r = rosary.Rosary(args.ip, args.port)

    r.register_effect(effects.sine_wave.SineWave)
    r.register_effect(effects.sine_wave.ThreePhaseSineWave)
    r.register_effect(effects.effect.SetColor)
    r.register_effect(effects.throb.Throb)
    r.register_effect(effects.bounce.Bounce)

    # create a bounce effect on all beads
    r.add_effect('bounce', r.Set_All)

    # change color to red
    r.effect(1).color.set(r.Color_Red)

    # add another throb on the odd beads
    r.add_effect('throb', r.Set_Odd_Ring, color=r.Color_Blue)

    # add bounce
    r.add_effect('bounce', r.Set_All, color=r.Color_Green)


    r.start()
    

    
