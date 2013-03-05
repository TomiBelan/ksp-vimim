
from __future__ import division

import sys
import pygame
import time


class Window(object):
    fps = 50

    def draw(self, ctx):
        pass

    def react(self, event):
        pass

    def start(self):
        pass

    def run(self, w, h, caption=None, fullscreen=False):
        pygame.display.init()
        pygame.font.init()

        self.w = w
        self.h = h

        flags = pygame.FULLSCREEN if fullscreen else 0
        screen = pygame.display.set_mode((w, h), flags)
        if caption: pygame.display.set_caption(caption)

        if sys.byteorder == 'little':
            screen.set_masks((0x00FF0000, 0x0000FF00, 0x000000FF, 0x00000000))
        else:
            # TODO: this might be wrong
            screen.set_masks((0x0000FF00, 0x00FF0000, 0xFF000000, 0x00000000))

        self.begin = time.time()
        self.running = True
        self.clock = pygame.time.Clock()
        self.start()
        while self.running:
            for event in pygame.event.get():
                self.react(event)
                if not self.running: return

            self.draw(screen)
            pygame.display.flip()
            if not self.running: return

            self.clock.tick(self.fps)


def draw_terminal(window, screensurf, screen):
    screensurf.fill([int(255 * f) for f in screen.mainbg])

    if not hasattr(window, 'terminal_font'):
        window.terminal_font = pygame.font.SysFont('DejaVu Sans Mono', 14)
        window.glyph_cache = {}
    line_height = window.terminal_font.get_linesize()

    for y, line in enumerate(screen.chars):
        fgline = screen.fg[y]
        bgline = screen.bg[y]
        sx = 0
        for x, char in enumerate(line):
            fg = fgline[x] or (1, 1, 1)
            bg = bgline[x]
            cid = (char, fg, bg)
            if cid not in window.glyph_cache:
                fgb = [int(255 * f) for f in fg]
                if bg:
                    bgb = [int(255 * f) for f in bg]
                    window.glyph_cache[cid] = window.terminal_font.render(char, True, fgb, bgb)
                else:
                    window.glyph_cache[cid] = window.terminal_font.render(char, True, fgb)
            screensurf.blit(window.glyph_cache[cid], (sx, y * line_height))
            sx += window.glyph_cache[cid].get_size()[0]

    fps = window.terminal_font.render('%.3ffps' % window.clock.get_fps(), True, (255, 255, 255))
    screensurf.blit(fps, (0, window.h - fps.get_size()[1]))

    if screen.flip:
        screensurf.blit(pygame.transform.flip(screensurf, True, True), (0, 0))


def draw_test(ctx):
    ctx.select_font_face('monospace')
    ctx.set_font_size(16)
    font_height = ctx.text_extents('0')[3]
    now = time.time() - window.begin

    ctx.set_source_rgb(1, 0.5, 0)
    ctx.arc(70 + now*20, 70 + now*5.5, 47, 0, 3.8)
    ctx.fill()
    ctx.arc(70 + now*20, 70 + now*5.5, 47, 4, -0.2)
    ctx.fill()

    ctx.save()
    ctx.set_source_rgb(1, 1, 1)
    ctx.translate(0, font_height)
    ctx.show_text('%.3f' % window.clock.get_fps())
    ctx.restore()


if __name__ == '__main__':
    window = Window()
    window.draw = draw_test
    window.run(800, 600, 'Hello')
