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

    r.add_effect('bounce', r.Set_All)


    r.start()
