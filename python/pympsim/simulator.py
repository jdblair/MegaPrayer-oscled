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
        self.spots = []
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
        y_position = 650
        blip_diameter = 4

        # directions to move
        up = [0, -1]
        down = [0, 1]
        right = [1, 0]
        left = [-1, 0]
        #lower_left_vertex = [-1, -1]
        lower_left_vertex = [0, -1]
        upper_left_vertex = [1, -1]
        upper_right_vertex = [1, 1]
        lower_right_vertex = [-1, 1]

        # cross piece lengths
        leg = 70
        neck = 26
        head = 14
        hand = 14
        arm_left = 54
        arm_right = 53
        vertex = 0

        blip_space = 1

        konami_code = [
                        [up, leg], [up, vertex], 
                        [left, arm_left], [left, vertex],
                        [up, hand], [up, vertex], 
                        [right, arm_left], [right, vertex],
                        [up, neck], [up, vertex], 
                        [right, head], [right, vertex],
                        [down, neck], [down, vertex],
                        [right, arm_right], [right, vertex],
                        [down, hand], [down, vertex],
                        [left, arm_right], [left, vertex],
                        [down, leg]
                       ]
        
        for move in konami_code:
            direction = move[0]
            length = move[1]
            
            delta_x = (blip_diameter + blip_space) * direction[0]
            delta_y = (blip_diameter + blip_space) * direction[1]


            # when we reach a vertex, don't add it to the blip set, just move the x and y position
            if (length == 0):
                x_position = x_position + delta_x
                y_position = y_position + delta_y

            else:
                n_blips = length
                for b in range(n_blips):
                    x_position = x_position + delta_x
                    y_position = y_position + delta_y

                    self.cross.append(
                        self.canvas.create_oval(x_position, y_position, 
                                                x_position + blip_diameter, y_position + blip_diameter, 
                                                fill="#128192200", width=0))



        # make the DMX / spotlights
        self.spots.append(self.canvas.create_polygon(190, 650, 205, 450, 290, 500, fill="white"))   
        self.spots.append(self.canvas.create_polygon(490, 650, 390, 500, 475, 450, fill="white"))


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
                if (iface_class == 'dmx'):
                    self.canvas.itemconfig(self.spots[num], fill=tk_rgb)
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
