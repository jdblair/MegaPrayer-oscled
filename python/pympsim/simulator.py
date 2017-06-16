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
        radius = 300
        bead_radius = 10
        stem_spacing = radius * pi * 2 / 56
        x_offset = radius + (stem_spacing * 4) + 50
        y_offset = 325
        self.beads = []
        #make the stem
        for i in range(0, 4):
            x = (x_offset - radius - stem_spacing * 4) + (stem_spacing * i)
            y = y_offset
            self.beads.append(self.canvas.create_oval(x, y, x+(2*bead_radius),y+(2*bead_radius), fill="#128192200", width=2))

        #make the rest of the beads
        for i in range(4, 60):
            angle = (pi * 2 / 56 * (i - 4)) - pi
            x = x_offset + radius * cos(angle)
            y = y_offset + radius * sin(angle)
            self.beads.append(self.canvas.create_oval(x, y, x+(2*bead_radius), y+(2*bead_radius), fill="#128192200", width=2))
        ##########################################################

        self.canvas.pack()

    # def updateBeads(self, beadData):
    #     for bd in beadData:
    #         bead = bd[0]
    #         r = int(bd[1] * 255)
    #         g = int(bd[2] * 255)
    #         b = int(bd[3] * 255)
    #         print(r,g,b)
    #         tk_rgb = "#%02x%02x%02x" % (r, g, b)
    #         self.canvas.itemconfig(self.beads[bead], fill=tk_rgb)

    def updateBeads(self, beadData):
        for bd in beadData:
            num = bd[0]
            length = bd[1]
            blob = bd[2]
            for i in range(0, len(blob), 6):
                #print(blob[i:i+6])
                (r, g, b) = unpack('!HHH', blob[i:i+6])
                tk_rgb = "#%02x%02x%02x" % (r >> 8, g >> 8, b >> 8)
                self.canvas.itemconfig(self.beads[num], fill=tk_rgb)
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
