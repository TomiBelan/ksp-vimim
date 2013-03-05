# -*- coding: utf-8 -*-

import time
import pygame
import random
from screen import Screen

STONE_CHANCE = 0.6
FORCE = 3

class Game(object):
    def __init__(self, vimim):
        self.vimim = vimim
        self.reset()

    def reset(self):
        self.enemies = [[random.random() < 1-0.1*x for y in xrange(24)] for x in xrange(80)]
        self.columns = [self.make_column() for x in xrange(80)]
        self.x = 55
        self.y = 12
        self.columns[self.x][self.y] = False
        self.ticks = 0
        self.speed = 10

    def draw(self, ctx):
        screen = Screen()
        for y in xrange(24):
            for x in xrange(80):
                if self.enemies[x][y]:
                    screen.chars[y][x] = u'\u2765'
                    screen.fg[y][x] = (1, 0, 0)
                elif x == self.x and y == self.y:
                    screen.chars[y][x] = u'@'
                    screen.fg[y][x] = (0, 0, 0)
                    screen.bg[y][x] = (0, 1, 0)
                elif self.columns[x][y]:
                    screen.chars[y][x] = u'O'
        if self.vimim.have_status_bar:
            self.vimim.draw_generic_status_bar(screen)
            screen.write(0, 24, u'-- GAME MODE --')
        # TODO isto ziaden postprocess?
        self.vimim.window.draw_terminal(self.vimim.window, ctx, screen)

    def keydown(self, event):
        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.vimim.bell()
            return

        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.move(-1, 0)
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_f:
            self.move(1, 0)
        elif event.key == pygame.K_UP or event.key == pygame.K_e:
            self.move(0, -1)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_x:
            self.move(0, 1)
        elif event.key == pygame.K_g:
            # free
            self.vimim.app = self.vimim.editor_app
        else:
            self.vimim.bell()

    def move(self, dx, dy):
        self.vimim.pay(4)   # TODO kalibrovat
        if not self.move_stone(self.x+dx, self.y+dy, dx, dy, FORCE): return
        self.x += dx
        self.y += dy
        if self.enemies[self.x][self.y]:
            self.win()

    def win(self):
        print "winrar!"   # DEBUG
        # TODO congratulation
        self.reset()

    def move_stone(self, x, y, dx, dy, force):
        if not ((0 <= x < 80) and (0 <= y < 24)): return False
        if not self.columns[x][y]: return True
        if force <= 0: return False
        if not self.move_stone(x+dx, y+dy, dx, dy, force-1): return False
        self.columns[x+dx][y+dy] = True
        self.columns[x][y] = False
        return True

    def idle(self):
        self.ticks += (4 if self.vimim.app == self else 3)
        if self.ticks >= self.speed*4:
            self.ticks -= self.speed*4
            self.columns.pop(0)
            self.columns.append(self.make_column())
            if self.x > 0: self.x -= 1
            if self.enemies[self.x][self.y]:
                self.win()

    def make_column(self):
        return [(random.random() < STONE_CHANCE) for y in xrange(24)]
