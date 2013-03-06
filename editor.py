# -*- coding: utf-8 -*-

import re
import time
import pygame
import random
import colorsys
from screen import Screen

corrections = u'for/fór bool/bol main/mamin until/nútil while/Chile char/cmar case/čase'
corrections = dict(s.split('/') for s in corrections.split())

class Editor(object):
    def __init__(self, vimim):
        self.vimim = vimim
        self.x = 0
        self.y = 0
        self.scroll = 0
        self.content = []
        self.undo_buffer = []
        self.mode = self.command_mode
        self.last_command = None
        self.highlight = { u' ': (0.7, 0.7, 0.7) }

    @property
    def height(self):
        return 24 if self.vimim.have_status_bar else 25

    def draw(self, ctx):
        screen = Screen()
        for y, line in enumerate(self.content[self.scroll:self.scroll+self.height]):
            screen.write(0, y, line[0:80])

        if self.vimim.features['highlight']:
            for y in xrange(self.height):
                for x in xrange(80):
                    ch = screen.chars[y][x]
                    if ch not in self.highlight:
                        self.highlight[ch] = colorsys.hsv_to_rgb(random.random(), 0.5*random.random()+0.5, 1)
                    screen.fg[y][x] = self.highlight[ch]

        if (0 <= self.y - self.scroll < self.height) and (0 <= self.x < 80) and not self.vimim.features['nocursor']:
            screen.bg[self.y - self.scroll][self.x] = screen.fg[self.y - self.scroll][self.x]
            screen.fg[self.y - self.scroll][self.x] = screen.mainbg

        if self.vimim.have_status_bar:
            self.vimim.draw_generic_status_bar(screen)
            screen.write(0, 24, self.mode.name)
        self.vimim.postprocess_screen(screen)
        self.vimim.window.draw_terminal(self.vimim.window, ctx, screen)

    def keydown(self, event):
        self.mode(event)

    def idle(self):
        self.vimim.game_app.idle()
        self.mode(None)

    def bell(self):
        self.vimim.bell()

    def pay(self):
        return self.vimim.pay(3)


    # ZAKLADNE UPRAVY

    def move_to(self, nx, ny):
        self.x = max(0, nx)
        self.y = max(0, ny)
        if self.y < self.scroll:
            self.scroll = self.y
        if self.y > self.scroll + self.height - 1:
            self.scroll = self.y - self.height + 1

    def move_by(self, dx, dy):
        self.move_to(self.x + dx, self.y + dy)

    def normalize(self, y, x):
        while len(self.content) <= y: self.content.append(u'')
        self.content[y] = self.content[y].rstrip().ljust(x)

    def normalize_line(self):
        self.normalize(self.y, 0)
        line = self.content[self.y]
        if self.x > len(line): self.move_to(len(line), self.y)
        return line

    def splice(self, y, xfrom, xto, replace=u''):
        self.normalize(y, xto)
        line = self.content[y]
        line = line[:xfrom] + replace + line[xto:]
        self.content[y] = line
        if y != self.y: return
        if xto - xfrom == len(replace): return
        if xfrom <= self.x < xto:
            self.move_to(xfrom + len(replace), self.y)
        elif (xfrom == xto and self.x == xfrom) or self.x >= xto:
            self.move_by(len(replace) - (xto - xfrom), 0)

    def newline(self, y=None, x=None):
        if y is None: y = self.y
        if x is None: x = self.x
        self.normalize(y, x)
        line = self.content[y]
        self.content.insert(y + 1, line[x:])
        self.content[y] = line[:x]
        if self.y < y or (self.y == y and self.x < x): return
        if self.y > y:
            self.move_by(0, 1)
        elif self.y == y and self.x >= x:
            self.move_by(-x, 1)

    def merge_line(self, y=None):
        if y is None: y = self.y
        if y == 0: return
        self.normalize(y-1, 0)
        self.normalize(y, 0)
        upper_line = self.content[y-1]
        self.content[y-1] += self.content[y]
        self.content.pop(y)
        if self.y == y:
            self.move_by(len(upper_line), -1)
        elif self.y > y:
            self.move_by(0, -1)

    def blank_char(self, y, x):
        if y < 0 or x < 0: return
        self.normalize(y, 0)
        if self.content[y][x:x+1] not in (u'', u' '):
            self.splice(y, x, x+1, u' ')

    def remember(self):
        self.undo_buffer.append((u'\n'.join(self.content), self.x, self.y))

    def undo(self):
        if self.undo_buffer:
            content, x, y = self.undo_buffer.pop()
            self.content = content.split(u'\n')
            self.move_to(x, y)


    # MODY

    def command_mode(self, event):
        if not event: return
        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.bell()
            return
        if not (pygame.K_a <= event.key <= pygame.K_z):
            self.bell()
            return
        if event.key not in (pygame.K_c, pygame.K_p):   # free
            if not self.pay(): return
        key = event.key
        if key == pygame.K_r:
            key = self.last_command
            if key is None: return

        def arrow(dx, dy):
            self.move_by(dx, dy)
            if self.vimim.features['horse']:
                self.move_by(dx, dy)
                self.move_by(dy * random.choice((-1, 1)), dx * random.choice((-1, 1)))

        if key == pygame.K_q:
            self.last_command = key
            self.vimim.darkness = time.time() + 30
        if key == pygame.K_w:
            self.last_command = key
            self.remember()
            line = self.normalize_line()
            self.splice(self.y, 0, len(line), line[::-1])
        if key == pygame.K_e:
            arrow(0, -1)
        if key == pygame.K_t:
            self.last_command = key
            self.remember()
            my_x = self.x
            my_line = self.normalize_line()
            while self.content and not self.content[-1].rstrip(): self.content.pop()
            self.content = sorted(line.rstrip() for line in self.content)
            self.content.sort()
            try:
                my_y = self.content.index(my_line)
            except ValueError:
                my_y = 0
            self.move_to(my_x, my_y)
        if key == pygame.K_y:
            self.last_command = key
            self.remember()
            self.mode = self.lottery_mode
        if key == pygame.K_u:
            self.last_command = None
            self.mode = self.undo_mode
        if key == pygame.K_i:
            self.last_command = key
            self.remember()
            self.mode = self.insert_mode
        if key == pygame.K_o:
            self.last_command = key
            self.remember()
            self.mode = self.overwrite_mode
        if key == pygame.K_p:
            self.last_command = key
            self.vimim.app = self.vimim.help_app
        if key == pygame.K_a:
            arrow(-1, 0)
        if key == pygame.K_s:
            self.last_command = key
            self.vimim.submit_app.open()
        if key == pygame.K_d:
            while self.content and not self.content[-1].rstrip(): self.content.pop()
            self.move_to(0, len(self.content))
        if key == pygame.K_f:
            arrow(1, 0)
        if key == pygame.K_g:
            self.last_command = key
            self.vimim.app = self.vimim.game_app
        if key == pygame.K_h:
            self.move_to(0, 0)
        if key == pygame.K_j:
            self.mode = self.jump_mode
        if key == pygame.K_k:
            self.normalize_line()
            self.move_to(len(self.content[self.y].rstrip()), self.y)
        if key == pygame.K_l:
            self.last_command = key
            self.remember()
            line = self.normalize_line()
            self.splice(self.y, 0, len(line), line.lower())
        if key == pygame.K_x:
            arrow(0, 1)
        if key == pygame.K_c:
            self.last_command = key
            self.vimim.config_app.open()
        if key == pygame.K_v:
            self.last_command = key
            self.remember()
            line = self.normalize_line()
            self.splice(self.y, 0, len(line), line.swapcase())
        if key == pygame.K_b:
            self.last_command = key
            self.remember()
            line = self.normalize_line()
            self.splice(self.y, 0, len(line) - len(line.lstrip()), u' ' * random.randint(0, 8))
        if key == pygame.K_n:
            self.move_to(random.randint(0, 79),
                         random.randint(self.scroll, self.scroll + self.height - 1))
        if key == pygame.K_m:
            self.last_command = key
            self.mode = self.delete_mode

    command_mode.name = u''


    def delete_mode(self, event):
        if not event: return
        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.bell()
            return
        if event.key not in [ord(c) for c in 'eropsvbzcnm']:
            self.bell()
            return
        if not self.pay(): return
        key = event.key

        if key == pygame.K_e:
            self.remember()
            self.merge_line()
        if key == pygame.K_r:
            self.remember()
            self.normalize(self.y, 0)
            self.content.pop(self.y)
            self.move_to(0, self.y)
        if key == pygame.K_o:
            self.remember()
            for (dx,dy) in ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)):
                self.blank_char(self.y + dy, self.x + dx)
        if key == pygame.K_p:
            self.remember()
            line = self.normalize_line()
            self.splice(self.y, 0, len(line), re.sub(ur'[A-Za-z]', u'', line).rstrip())
        if key == pygame.K_s:
            self.remember()
            self.normalize_line()
            prefix = self.content[self.y][0:self.x]
            self.splice(self.y, 0, len(prefix), re.sub(ur'(\w+|\W+)$', u'', prefix))
        if key == pygame.K_v:
            self.remember()
            self.content = []
            self.move_to(0, 0)
        if key == pygame.K_b:
            self.remember()
            pass # TODO
        if key == pygame.K_z:
            self.remember()
            line = self.normalize_line()
            self.splice(self.y, 0, len(line), re.sub(ur'[\(\)\[\]{}]', u'', line).rstrip())
        if key == pygame.K_c:
            self.remember()
            line = self.normalize_line()
            self.splice(self.y, 0, len(line), re.sub(ur'[0-9]', u'', line).rstrip())
        if key == pygame.K_n:
            self.remember()
            self.normalize_line()
            prefix = self.content[self.y][0:self.x]
            self.splice(self.y, 0, len(prefix), prefix[0:random.randint(0, len(prefix))])
        if key == pygame.K_m:
            self.mode = self.command_mode

    delete_mode.name = u'-- MAŽEM MODE --'


    def insert_mode(self, event):
        if not event:
            if self.vimim.features['spellcheck'] and random.randint(0, 4) == 0:
                self.normalize(self.y, self.x)
                for key in corrections:
                    if self.content[self.y][self.x-len(key):self.x] == key:
                        self.splice(self.y, self.x-len(key), self.x, corrections[key])
            return

        code = event.unicode
        if code == u'\t': code = u' '
        for i in xrange(2 if self.vimim.features['double'] else 1):
            if code.lower() == u'i':
                # free
                self.mode = self.command_mode
                return
            elif code == u'\n':
                if not self.pay(): return
                if self.vimim.features['japan']:
                    self.move_to(self.x - 1, 0)
                else:
                    self.newline()
            elif code and ord(code[0]) >= 32:
                if not self.pay(): return
                if self.vimim.features['japan']:
                    self.splice(self.y, self.x, self.x + len(code), code)
                    self.move_by(0, 1)
                else:
                    self.splice(self.y, self.x, self.x, code)
            else:
                self.bell()
                return

        if self.vimim.features['parens']:
            pairs = dict(zip(u'([{<"\'', u')]}>"\''))
            if code in pairs:
                self.splice(self.y, self.x, self.x, pairs[code])
                self.move_by(-1, 0)

    insert_mode.name = u'-- INSERT MODE --'


    def overwrite_mode(self, event):
        if not event: return

        if event.unicode.lower() == u'o':
            # free
            self.mode = self.command_mode
        elif len(event.unicode) == 1 and ord(event.unicode) >= 32:
            if not self.pay(): return
            self.splice(self.y, self.x, self.x + 1, event.unicode)
        else:
            self.bell()

    overwrite_mode.name = u'-- OPRAVUJEM MODE --'


    def lottery_mode(self, event):
        if not event:
            self.splice(self.y, self.x, self.x + 1, unichr(random.randint(32, 126)))
            return

        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.bell()
            return
        self.mode = self.command_mode

    lottery_mode.name = u'-- LOTÉRIA MODE --'


    def jump_mode(self, event):
        if not event: return

        if len(event.unicode) == 1 and ord(event.unicode) >= 32:
            best = (float('inf'), 0, self.y, self.x)
            for y, line in enumerate(self.content):
                for x, ch in enumerate(line):
                    if ch == event.unicode:
                        dist = (y - self.y)**2 + (x - self.x)**2
                        best = min(best, (dist, abs(y - self.y), y, x))
            self.move_to(best[3], best[2])
            self.mode = self.command_mode
        else:
            self.bell()

    jump_mode.name = u'jump to:'


    def undo_mode(self, event):
        if not event:
            self.undo()
            self.undo()
            return

        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.bell()
            return
        if event.key == pygame.K_u:
            self.undo()
            self.undo()
            self.undo()
            self.mode = self.command_mode
        else:
            self.bell()

    undo_mode.name = u'-- UNDO MODE --'
