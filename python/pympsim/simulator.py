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

        self.canvas = Canvas(master, width=1500, height=700, borderwidth=0, highlightthickness=0, bg="black")

        ############### John's fancy witchcraft ###################
        i = 0
        stem_beads = 5
        ring_beads = 60 - stem_beads
        radius = 300
        bead_radius = 10
        stem_spacing = radius * pi * 2 / ring_beads
        stem_length = stem_spacing * stem_beads
        x_offset = radius + stem_length + 600
        y_offset = 325
        lords_gap_ratio = 0.2
        self.beads = []
        self.bases = []
        self.cross = [] 
        # make the stem
        x = (x_offset - radius - stem_length) + (stem_spacing * i)
        for i in range(0, 5):
            y = y_offset
            self.beads.append(self.canvas.create_oval(x, y, x+(2*bead_radius),y+(2*bead_radius), fill="#128192200", width=2))
            x += stem_spacing

        # make the rest of the beads
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

        # make the bases
        for i in range(0, 9):
            angle = (pi * 2 / 9 * (i - 5)) - pi
            x = x_offset + (radius - (bead_radius * 3)) * cos(angle)
            y = y_offset + (radius - (bead_radius * 3)) * sin(angle)


            self.bases.append(
                self.canvas.create_polygon((x + bead_radius, y,
                                            x, y + (2 * bead_radius),
                                            x + (2 * bead_radius), y + (2 * bead_radius)),
                                           fill="#128192200", width=2))

        # make the cross -- would like to have this in a separate window somedaaaaay
        # this algorithm prolly just obfuscates the code but i like it anyway
        x_position = 300
        y_position = 615
        blip_diameter = 4

        up = [0, -1]
        down = [0, 1]
        right = [1, 0]
        left = [-1, 0]

        leg = 75
        neck = 28
        head = 18
        hand = 18
        arm = 55

        konami_code = [up, left, up, right, up, right, down, right, down, left, down]
        blip_count = [leg, arm, hand, arm, neck, head, neck, arm, hand, arm, leg]
        
        for i, move in enumerate(konami_code):
            delta_x = (blip_diameter + 1) * move[0]
            delta_y = (blip_diameter + 1) * move[1]
            n_blips = blip_count[i]
            for b in range(n_blips):
                self.cross.append(
                    self.canvas.create_oval(x_position, y_position, 
                                            x_position - blip_diameter, y_position - blip_diameter, 
                                            fill="white", width=0))

                x_position = x_position + delta_x
                y_position = y_position + delta_y 
 
        '''
        # cross base, left side, drawing from bottom to top

        for p in range(75):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset - 4, y_offset - 4, 
                                        fill="red", width=0))
            y_offset = y_offset - 5
        
        # cross arm, left side, drawing from right to left
        for p in range(55):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset - 4, y_offset - 4, 
                                        fill="red", width=0))
            x_offset = x_offset - 5

        # cross arm, left side, drawing from bottom to top
        for p in range(18):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset - 4, y_offset - 4, 
                                        fill="red", width=0))
            y_offset = y_offset - 5

        # cross arm, left side, drawing from left to right
        for p in range(55):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0))
            x_offset = x_offset + 5

        # cross head, left side, drawing from bottom to top
        for p in range(28):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0))
            y_offset = y_offset - 5

        # cross head, across the top, drawing from left to right
        for p in range(18):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0))
            x_offset = x_offset + 5

        # cross head, right side, drawing from top to bottom
        for p in range(28):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0))
            y_offset = y_offset + 5

        # cross arm, right side, drawing from left to right
        for p in range(55):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0))
            x_offset = x_offset + 5

        # cross arm, right side, drawing from top to bottom
        for p in range(18):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0))
            y_offset = y_offset + 5

        # cross arm, right side, drawing from right to left
        for p in range(55):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0))
            x_offset = x_offset - 5
        
        # cross base, right side, drawing from top to bottom
        for p in range(75):
            self.cross.append(
                self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0))
            y_offset = y_offset + 5

        # cross base, across the bottom, drawing from right to left
        y_offset = y_offset + 80 #this is to adjust for removing the 17 blips to save power
        for p in range(18):
            #these aren't appended to the cross array, just a placeholder
            #to demonstrate where the base of the cross is
            self.canvas.create_oval(x_offset, y_offset, 
                                        x_offset + 4, y_offset + 4, 
                                        fill="red", width=0)
            x_offset = x_offset - 5
'''
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
                if (iface_class == 'cross'):
                    self.canvas.itemconfig(self.cross[num], fill=tk_rgb)
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
