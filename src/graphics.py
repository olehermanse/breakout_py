#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""graphics primitives"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

import math

try:
    import pyglet
    from pyglet.text import Label
    from pyglet.resource import image
except:
    print("Warning: could not import pyglet")

class Color:
    colors = {
        "red":   (255,0,0,255),
        "green": (0,255,0,255),
        "blue":  (0,0,255,255),
        "white": (255,255,255,255),
        "black": (0,0,0,255)
    }
    @classmethod
    def get(cls, name):
        return cls.colors[name]

def start_rendering(window):
    window.clear()
    pyglet.gl.glClearColor(255,255,255,255)

def update_pos(obj):
    obj.x, obj.y = obj.x + obj.dx, obj.y + obj.dy

def update_vel(obj):
    obj.dx, obj.dy = obj.dx + obj.ddx, obj.dy + obj.ddy

def limit(number, lower, upper):
    if number < lower:
        return lower
    if number > upper:
        return upper
    return number

class Text:
    def __init__(self, text, pos, size=12, font_name="Helvetica"):
        self.label = Label(text, font_name=font_name, font_size=size,
                                 x=pos[0], y=pos[1], color=Color.get("black"),
                                 anchor_x="left", anchor_y="bottom",
                                 multiline=True, width = 500)

    def draw(self):
        self.label.draw()

class Rectangle:
    def __init__(self, width, height, pos=(0,0), vel=(0,0), acc=(0,0),
                 fill=(128,128,128,255), stroke=(0,0,0,0)):
        self.w = width
        self.h = height
        self.set_pos(*pos)
        self.set_vel(*vel)
        self.set_acc(*acc)
        self.stroke = stroke
        self.fill = fill
        self.visible = True

    def set_pos(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def set_vel(self, dx, dy):
        self.dx = float(dx)
        self.dy = float(dy)

    def set_vel_angle(self, angle, speed):
        angle = angle * math.pi / 180
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def get_vel_angle(self):
        angle = math.atan2(self.dy, self.dx)
        angle = angle * 180 / math.pi
        return angle

    def set_speed(self, speed):
        angle = self.get_vel_angle()
        self.set_vel_angle(angle, speed)

    def set_acc(self, ddx, ddy):
        self.ddx = float(ddx)
        self.ddy = float(ddy)

    # Note: if you don't need acceleration and velocity
    #       simply call set_pos instead
    def update(self, dt):
        s = self

        dt = float(dt)
        # Do all calculations first (right side) then assign (left side):
        x, y, dx, dy = float(s.x  + dt*s.dx),  \
                       float(s.y  + dt*s.dy),  \
                       float(s.dx + dt*s.ddx), \
                       float(s.dy + dt*s.ddy)
        # Sub classes can override these methods, like robot does:
        self.set_vel(dx,dy)
        self.set_pos(x,y)

    def set_fill(self, fill):
        self.fill = fill

    def contains(self, x, y):
        if x >= self.x and x <= self.x + self.w and \
           y >= self.y and y <= self.y + self.h:
           return True
        return False

    def get_vertices(self):
        return [(self.x, self.y), (self.x+self.w, self.y),
                (self.x+self.w, self.y+self.h), (self.x, self.y+self.h)]

    def draw(self):
        if not self.visible:
            return
        pyglet.gl.glLineWidth(4)
        rect_vertices = pyglet.graphics.vertex_list(4,
            ('v2f', (self.x,        self.y) +
                    (self.x+self.w, self.y) +
                    (self.x+self.w, self.y+self.h) +
                    (self.x,        self.y+self.h)
            ),
            ('c4B', self.fill * 4)
        )
        rect_vertices.draw(pyglet.gl.GL_QUADS)

        rect_vertices.colors = self.stroke * 4
        rect_vertices.draw(pyglet.gl.GL_LINE_LOOP)

    def collides_with(self, rect):
        for coord in self.get_vertices():
            if rect.contains(*coord):
                return True
        return False

    def collision(self, rect, seq):
        verts = self.get_vertices()
        rval = False
        for index in range(4):
            coord = verts[index]
            if rect.contains(*coord):
                seq[index] = True
                rval = True
        return rval
