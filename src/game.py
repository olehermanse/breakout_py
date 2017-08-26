#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""breakout game class"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE'

from graphics import Text, Rectangle, start_rendering, limit

import random

def stupid_ai(game):
    left = right = False
    if game.ball.x < game.player.x:
        left = True
    elif game.ball.x + game.ball.w > game.player.x + game.player.w:
        right = True
    return left,right

class Game:
    def __init__(self, window, width, height, rows, columns, wall_height):
        self.window = window
        self.bricks = []
        self.w = width
        self.h = height
        self.player = Rectangle(100, 25, fill=(255,128,128,255))
        self.ball = Rectangle(25, 25, fill=(128,128,255,255))
        self.generate_bricks(width, wall_height, rows, columns)
        self.debug_info = Text("Temp", font_name="Courier", pos=(25,25))
        self.speed_multiplier = 6.0
        self.reset()

    def generate_bricks(self, wall_width, wall_height, rows, columns):
        brick_width = wall_width / columns
        brick_height = wall_height / rows

        for r in range(rows):
            y = 600 - brick_height - brick_height * r
            for c in range(columns):
                x = brick_width * c
                brick = Rectangle(brick_width, brick_height, pos=(x,y))
                self.bricks.append(brick)

    def reset_ball(self):
        self.ball.set_pos(388,288)
        self.ball.speed = 200.0
        down_angle = random.uniform(0, 90)
        self.ball.set_vel_angle(225 + down_angle, self.ball.speed)

    def reset_player(self):
        self.player.set_pos(350,0)
        self.player.speed = 250.0

    def reset(self):
        self.left_key = self.right_key = False
        self.score = 0
        self.reset_player()
        self.reset_ball()
        for b in self.bricks:
            b.visible = True

    def game_over(self):
        self.reset()

    def crush_brick(self, brick):
        brick.visible = False
        self.score += 1
        self.ball.speed += 10

    # TODO: change to batch drawing for performance
    def draw(self):
        start_rendering(self.window)
        self.debug_info.draw()
        self.player.draw()
        self.ball.draw()
        for b in self.bricks:
            b.draw()

    def update_debug_info(self):
        msg =  "Score      = {}" \
             "\nplayer     = {:8.2f},{:8.2f}" \
             "\nball       = {:8.2f},{:8.2f}" \
             "\nball_speed = {:8.2f}" \
             "\nball_vel   = {:8.2f},{:8.2f}".format(
                             self.score,
                             self.player.x, self.player.y,
                             self.ball.x,   self.ball.y,
                             self.ball.speed,
                             self.ball.dx,  self.ball.dy)
        self.debug_info.label.text = msg

    def update(self, dt):
        dt *= self.speed_multiplier
        player = self.player
        ball = self.ball

        ball.update(dt)
        player.update(dt)

        player.set_pos(limit(player.x, 0, 700), player.y)

        self.left_key, self.right_key = stupid_ai(self)
        if self.left_key and not self.right_key:
            player.dx = - self.player.speed
        elif self.right_key and not self.left_key:
            player.dx = self.player.speed
        else:
            player.dx = 0


        collisions = [False] * 4
        for brick in self.bricks:
            if brick.visible:
                if ball.collision(brick, collisions):
                    self.crush_brick(brick)
        if True in collisions:
            n = ""
            for x in collisions:
                if x:
                    n += "1"
                else:
                    n += "0"
            if "1" in n:
                if n == "1100":
                    self.ball.dy = - self.ball.dy
                if n == "0011":
                    self.ball.dy = - self.ball.dy
                if n == "1001":
                    self.ball.dx = - self.ball.dx
                if n == "0110":
                    self.ball.dx = - self.ball.dx
                if sum([int(c) for c in n]) == 1:
                    self.ball.dx = - self.ball.dx
                    self.ball.dy = - self.ball.dy

        if ball.collides_with(player) and ball.dy < 0:
            ball.dy = - ball.dy
            ball.dx += 0.5 * player.dx

        if ball.x < 0 and ball.dx < 0:
            ball.dx = - ball.dx
        if ball.y < 0:
            self.game_over()
        if ball.x + ball.w > 800 and ball.dx > 0:
            ball.dx = - ball.dx
        if ball.y + ball.h > 600 and ball.dy > 0:
            ball.dy = - ball.dy

        self.ball.speed += dt
        self.ball.set_speed(self.ball.speed)

        self.update_debug_info()
