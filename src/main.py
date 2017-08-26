#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""entry point and pyglet events"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from game import Game

try:
    import pyglet
    from pyglet.graphics import glScalef
    from pyglet.window import mouse
    import pyglet.window.key as key
except:
    print("Warning: could not import pyglet")

def update(dt):
    game.update(dt)

if __name__ == '__main__':
    window = pyglet.window.Window(800,600, resizable=False)
    game = Game(window, 800, 600, rows=6, columns=10, wall_height=240)
    pyglet.clock.schedule_interval(update, 0.005) # 200 updates per sec

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.LEFT:
            game.left_key = True
        elif symbol == key.RIGHT:
            game.right_key = True

    @window.event
    def on_key_release(symbol, modifiers):
        if symbol == key.LEFT:
            game.left_key = False
        elif symbol == key.RIGHT:
            game.right_key = False

    @window.event
    def on_draw():
        game.draw()

    pyglet.app.run()
