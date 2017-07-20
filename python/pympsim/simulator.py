#!/usr/bin/python3
import math
import time

from tkinter import *
from math import pi
from math import cos
from math import sin
from struct import unpack


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.canvas = Canvas(master, width=900, height=700, borderwidth=0, highlightthickness=0, bg="black")

        ###############John's fancy witchcraft ###################
        i = 0
        stem_beads = 5
        ring_beads = 60 - stem_beads
        radius = 300
        bead_radius = 10
        stem_spacing = radius * pi * 2 / ring_beads
        stem_length = stem_spacing * stem_beads
        x_offset = radius + stem_length + 50
        y_offset = 325
        lords_gap_ratio = 0.2
        self.beads = []
        self.bases = []
        #make the stem
        x = (x_offset - radius - stem_length) + (stem_spacing * i)
        for i in range(0, 5):
            y = y_offset
            self.beads.append(self.canvas.create_oval(x, y, x+(2*bead_radius),y+(2*bead_radius), fill="#128192200", width=2))
            x += stem_spacing

        #make the rest of the beads
        bead_spacing = (pi * 2) / (ring_beads + 1)   # there's an "extra" empty bead at the junction
        # remove a little from bead_spacing to make room for the extra space around lords prayer beads
        bead_spacing -= (bead_spacing * bead_radius * lords_gap_ratio) / (ring_beads + 1)
        angle = 0 - pi + bead_spacing
        for i in range(5, 60):
            x = x_offset + radius * cos(angle)
            y = y_offset + radius * sin(angle)
            self.beads.append(self.canvas.create_oval(x, y, x+(2*bead_radius), y+(2*bead_radius), fill="#128192200", width=2))
            if i in [9, 10, 20, 21, 31, 32, 42, 43, 53, 54]:
                angle += bead_spacing * lords_gap_ratio
            angle += bead_spacing

        #make the bases
        for i in range(0, 9):
            angle = (pi * 2 / 9 * (i - 6)) - pi
            x = x_offset + (radius - (bead_radius * 3)) * cos(angle)
            y = y_offset + (radius - (bead_radius * 3)) * sin(angle)


            self.bases.append(
                self.canvas.create_polygon((x + bead_radius, y,
                                            x, y + (2 * bead_radius),
                                            x + (2 * bead_radius), y + (2 * bead_radius)),
                                           fill="#128192200", width=2))

#self.canvas.create_oval(x, y, x+(2*bead_radius), y+(2*bead_radius), fill="#128192200", width=2))


        ##########################################################

        self.canvas.pack()


    def updateBeads(self, beadData):
        bead_len = 8
        for bd in beadData:
            iface_class = bd[0]
            num = bd[1]
            length = bd[2]
            blob = bd[3]
            for i in range(0, len(blob), bead_len):
                #print(blob[i:i+6])
                (r, g, b, brightness) = unpack('!HHHH', blob[i:i+bead_len])
                tk_rgb = "#%02x%02x%02x" % (r >> 8, g >> 8, b >> 8)
                if (iface_class == 'rosary'):
                    self.canvas.itemconfig(self.beads[num], fill=tk_rgb)
                if (iface_class == 'base'):
                    self.canvas.itemconfig(self.bases[num], fill=tk_rgb)
                num += 1



def main(queue):
    animation = Tk()
    app = App(animation)

    while True:
        msg = queue.get()         # Read from the queue and do nothing
        if (msg):
            animation.update_idletasks()
            animation.update()
            #print(msg)
            app.updateBeads(msg)
