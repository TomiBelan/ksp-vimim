# -*- coding: utf-8 -*-

import pygame
from screen import Screen

class Problem(object):
    SAVE = []

    def __init__(self, vimim):
        self.vimim = vimim

    def open(self, text=None):
        self.vimim.app = self
        self.scroll = 0
        self.after_submit = (text is not None)

        if text is None:
            tasknum = self.vimim.submit_app.task
            taskname = self.vimim.task_names[tasknum]
            if tasknum == len(self.vimim.task_names):
                text = u'Už máš všetky úlohy. Gratulujeme.'
            else:
                with open('testovac/task_data/%s/desc' % taskname) as f:
                    text = f.read().decode('utf-8')

        self.text = []
        for line in text.split(u'\n'):
            if not line: self.text.append(line)
            for i in xrange(0, len(line), 80):
                self.text.append(line[i:i+80])

    def draw(self, ctx):
        screen = Screen()
        for y in xrange(self.vimim.editor_app.height):
            if self.scroll + y < len(self.text):
                screen.write(0, y, self.text[self.scroll + y])
        if self.vimim.have_status_bar:
            self.vimim.draw_generic_status_bar(screen)
            screen.write(0, 24, u'-- SUBMIT MODE --' if self.after_submit else u'-- ZADANIE MODE --')
        self.vimim.postprocess_screen(screen)
        self.vimim.window.draw_terminal(self.vimim.window, ctx, screen)

    def keydown(self, event):
        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.vimim.bell()
            return
        if event.key == pygame.K_UP or event.key == pygame.K_e:
            if self.scroll: self.scroll -= 1
        elif event.key == pygame.K_DOWN or event.key == pygame.K_x:
            self.scroll += 1
        elif event.key == (pygame.K_s if self.after_submit else pygame.K_z):
            self.vimim.app = self.vimim.editor_app
        else:
            self.vimim.bell()

    def idle(self):
        self.vimim.game_app.idle()


