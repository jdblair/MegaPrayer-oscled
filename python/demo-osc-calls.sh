#/bin/sh

# NOTE: Not meant to be run as a script. Just in .sh format so it'd be obvious from the outside that these are command line commands.

# Check paths on start (Not returned, check server.py's prints)
oscsend localhost 5006 /paths

# Add an effect, trivial case
oscsend localhost 5006 /rosary/add_effect s bounce

# Add an effect with color name
oscsend localhost 5006 /rosary/add_effect sss bounce all red

# Add an effect with rgb
oscsend localhost 5006 /rosary/add_effect ssiff bounce all 1 .5 .7

# Check paths
oscsend localhost 5006 /paths

# Clear effects
oscsend localhost 5006 /rosary/clear_effects

# Check that paths unregistered
oscsend localhost 5006 /paths
