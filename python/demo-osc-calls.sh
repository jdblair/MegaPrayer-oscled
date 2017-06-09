#/bin/sh

# NOTE: Not meant to be run as a script. Just in .sh format so it'd be obvious from the outside that these are command line commands.

# Check paths on start (Not returned, check server.py's prints)
oscsend localhost 5006 /paths

# Add an effect, trivial case
oscsend localhost 5006 /rosary/add_effect/name/bounce

# Paths are updated with available knobs for ALL running effects
oscsend localhost 5006 /paths

# Set running bounce's color
oscsend localhost 5006 /effect/set_color/r/1.0/g/0.0/b/0.0

# Set running bounce's direction
oscsend localhost 5006 /effect/set_direction/direction/1

# Fade the bounce out
oscsend localhost 5006 /effect/fade_out/fade_duration/30

# Add a green casino effect
oscsend localhost 5006 /rosary/add_effect/name/casino/r/0.0/g/1.0/b/0.0

# Change the color to cyan
oscsend localhost 5006 /effect/set_color/r/0.0/g/1.0/b/1.0

# Change the direction (and blow up the rosary)
oscsend localhost 5006 /effect/set_direction/direction/-1
