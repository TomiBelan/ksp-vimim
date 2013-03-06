# -*- coding: utf-8 -*-

import time
import pygame
import random
from config import feature_names
from screen import Screen

STONE_CHANCE = 0.6
FORCE = 3

class Game(object):
    SAVE = ['enemies', 'columns', 'x', 'y', 'ticks', 'speed', 'price_move',
        'ticks_newspeed', 'ticks_newspeed_choices', 'speed_choices']

    def __init__(self, vimim):
        self.vimim = vimim
        self.win_item = None
        self.win_time = 0
        self.price_move = 1
        self.ticks_newspeed_choices = [10, 20, 30, 40, 50, 60]
        self.speed_choices = [5, 10, 15, 20, 30, 40, 50]
        self.reset()

    def reset(self):
        self.enemies = [[random.random() < 1-0.1*x for y in xrange(24)] for x in xrange(80)]
        self.columns = [self.make_column() for x in xrange(80)]
        self.x = 55
        self.y = 12
        self.columns[self.x][self.y] = False
        self.ticks = 0
        self.speed = 10
        self.ticks_newspeed = 0

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
        self.vimim.postprocess_screen(screen, ingame=True)
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
        if not self.vimim.pay(self.price_move): return
        if not self.move_stone(self.x+dx, self.y+dy, dx, dy, FORCE): return
        self.x += dx
        self.y += dy
        if self.enemies[self.x][self.y]:
            self.win()

    def choose_speed(self):
        self.ticks = 0
        self.speed = (80 if self.vimim.submit_app.task == 0 else random.choice(self.speed_choices))
        self.ticks_newspeed = 20 * random.choice(self.ticks_newspeed_choices)

    def win(self):
        print "winrar!"
        inactive = [fid for (fid, value) in self.vimim.features.iteritems() if not value]
        if inactive:
            if self.vimim.submit_app.task == 0:
                for zfid in ('japan', 'double', 'nocursor'):
                    if zfid in inactive: inactive.remove(zfid)
            fid = random.choice(inactive)
            print "zapinam.odmenu", fid
            self.vimim.features[fid] = True
            self.win_item = fid
            self.win_time = time.time() + 8
        self.reset()

    def congratulate(self, screen):
        lines = [
            u'VYHRAL SI GAME MODE! :D',
            u'Za odmenu dostávaš fičúriu:',
            u'"%s"' % feature_names[self.win_item]
        ]
        left = 20
        right = 79 - 20
        top = 16
        bottom = 20
        for y in xrange(top, bottom+1):
            for x in xrange(left, right+1):
                if y == top or y == bottom or x == left or x == right:
                    screen.chars[y][x] = '+'
                    screen.fg[y][x] = random.choice([(1,0,0), (0,1,0), (0,0,1)])
                else:
                    screen.chars[y][x] = '-'
                    screen.fg[y][x] = (0, 0, 0)
                screen.bg[y][x] = (1, 1, 1)
        for i in xrange(len(lines)):
            width = right - left - 1
            screen.write(left+1, top+1+i, lines[i][0:width].center(width))

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
        self.ticks_newspeed -= 1
        if self.ticks_newspeed <= 0:
            self.choose_speed()

    def make_column(self):
        return [(random.random() < STONE_CHANCE) for y in xrange(24)]
