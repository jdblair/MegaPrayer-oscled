#/bin/sh

# This file is actually meant to be executed
# Should fade out when you Ctrl+C

while :
do
    oscsend localhost 5006 /input/left_nail
    # Or this
    #oscsend localhost 5006 /input/some_other_thing
    sleep 1
done
