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

    #r.add_effect_object(effects.Effect_Bounce(r.Set_All, color=color.ColorFade(start=r.Color_Green, finish=r.Color_Violet)))

    #id = r.add_effect('sine_wave', r.Set_Ring);
    #r.effect(id).color = ColorFade(start=r.Color_Red, finish=r.Color_Blue)
    r.start()

#    r.add_effect(Effect_SineWave(r.Set_Half01, color=Color(1, 1, 0), period=2, direction=-1))
#    r.add_effect(Effect_SineWave(r.Set_Half23, color=Color(0, 1, 1), period=2, direction=1))

#    r.add_effect(Effect_Bounce(r.Set_Ring, color=r.Color_Violet))
#    r.add_effect(Effect_Bounce(r.Set_Ring, color=r.Color_Yellow, direction=-1))
#    r.add_effect(Effect_Bounce(r.Set_Ring, color=r.Color_Violet))
#    r.add_effect(Effect_Bounce(r.Set_Ring, color=r.Color_Violet))x

#    r.add_effect(Effect_Bounce(r.Set_Eighth0, color=r.Color_Red))
#    r.add_effect(Effect_Bounce(r.Set_Eighth1, color=r.Color_Red))
#    r.add_effect(Effect_Bounce(r.Set_Eighth2, color=r.Color_Red))
#    r.add_effect(Effect_Bounce(r.Set_Eighth3, color=r.Color_Red))
#    r.add_effect(Effect_Bounce(r.Set_Eighth4, color=r.Color_Blue, direction=-1))
#    r.add_effect(Effect_Bounce(r.Set_Eighth5, color=r.Color_Blue, direction=-1))
#    r.add_effect(Effect_Bounce(r.Set_Eighth6, color=r.Color_Blue, direction=-1))
#    r.add_effect(Effect_Bounce(r.Set_Eighth7, color=r.Color_Blue, direction=-1))

#    r.add_effect(Effect_ThreePhaseSineWave(r.Set_Stem | r.Set_Eighth7 | r.Set_Eighth0, Color(1, 1, 1), period=1, direction=1))
#    r.add_effect(Effect_ThreePhaseSineWave(r.Set_Odd_All, Color(1, 1, 1), period=3, direction=1))
#    r.add_effect(Effect_ThreePhaseSineWave(r.Set_Even_All, Color(1, 1, 1), period=3, direction=-1))
#    r.add_effect(Effect_ThreePhaseSineWave(r.Set_All, Color(1, 1, 1), period=3, direction=-1))


