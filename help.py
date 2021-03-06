# -*- coding: utf-8 -*-

import pygame
from screen import Screen

class Help(object):
    SAVE = []

    def __init__(self, vimim):
        self.vimim = vimim

    def draw(self, ctx):
        screen = Screen()
        for y, line in enumerate(help_lines[0:24]):
            screen.write(0, y, line[0:80])
        if self.vimim.have_status_bar:
            self.vimim.draw_generic_status_bar(screen)
            screen.write(0, 24, u'-- POMOCNÍK MODE --')
        self.vimim.postprocess_screen(screen)
        self.vimim.window.draw_terminal(self.vimim.window, ctx, screen)

    def keydown(self, event):
        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.vimim.bell()
            return
        if event.key == pygame.K_p:
            self.vimim.app = self.vimim.editor_app
        else:
            self.vimim.bell()

    def idle(self):
        self.vimim.game_app.idle()


help_text = u'''

    VIMIM - Vi Improved Improved


    Základné príkazy:

    C = Config fičúrií a zadávanie kupónov
    G = Game mode
    P = Pomocník zap/vyp
    S = Submitúúúj
    U = Undo mode


    Čo nič nerobí:

  * Escape nič nerobí
  * Meta nič nerobí
  * Alt nič nerobí
  * Ctrl nič nerobí
  * Super/Win nič nerobí
  * myš nič nerobí
  * príkazy sú iba písmená a nezáleží na veľkosti

'''
help_lines = help_text.split(u'\n')[1:]
