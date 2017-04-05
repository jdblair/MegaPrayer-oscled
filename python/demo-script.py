# create a throb effect on all beads
r.add_effect('throb', r.Set_All)

# creates effect id 1

# change color to red
r.effect(1).color.set(r.Color_Red)

# change period to 2
r.effect(1).period=2

# change period to 5
r.effect(1).period=5

# change period to .5
r.effect(1).period=.5

# change bead set
r.effect(1).set_bead_set(r.Set_Ring)
# changes to ring, leaves stem in old state

# change bead set again
r.effect(1).set_bead_set(r.Set_Even_Ring)

# add another throb on the odd beads
r.add_effect('throb', r.Set_Odd_Ring, color=r.Color_Blue)

# add bounce
r.add_effect('bounce', r.Set_All, color=r.Color_Green)

# change to ring
r.effect(3).set_bead_set(r.Set_Ring)

# add more bounce
r.add_effect('bounce', r.Set_Ring, color=r.Color_Yellow)
r.add_effect('bounce', r.Set_Ring, color=r.Color_Violet)

# add a bunch more, using up-arrow

# remove one
r.del_effect(5)

# add a sine_wave to the stem
r.add_effect('sine_wave', r.Set_Stem)

# clear all the effects
r.clear_effects()

# create a sine_wave effect
r.add_effect('sine_wave', r.Set_All)

r.effect(9).period=2
r.effect(9).period=3
r.effect(9).period=4

r.effect(9).direction=-1
r.effect(9).direction=1
r.effect(9).direction=-1

r.effect(9).period=1
r.effect(9).direction=2
r.effect(9).direction=3

r.del_effect(1)

