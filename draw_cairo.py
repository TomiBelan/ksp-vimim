
from __future__ import division

import sys
import cairo
import pygame
import time
import math


class Window(object):
    fps = 50

    background = (0, 0, 0)

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

        def draw_internal():
            screen.fill(self.background)

            # screendata must not be in scope anymore when doing flip()
            screendata = pygame.surfarray.pixels2d(screen).data
            csurf = cairo.ImageSurface.create_for_data(
                    screendata, cairo.FORMAT_RGB24, w, h)
            ctx = cairo.Context(csurf)
            self.draw(ctx)

        self.begin = time.time()
        self.running = True
        self.clock = pygame.time.Clock()
        self.start()
        while self.running:
            draw_internal()
            pygame.display.flip()
            if not self.running: return

            for event in pygame.event.get():
                self.react(event)
                if not self.running: return

            self.clock.tick(self.fps)


def draw_terminal(window, ctx, screen):
    ctx.select_font_face('monospace')
    ctx.set_font_size(15)
    ascent, descent, font_height, max_x_advance, max_y_advance = ctx.font_extents()

    ctx.save()
    ctx.set_source_rgb(1, 1, 1)
    ctx.translate(0, -descent)
#    ctx.rotate(0.5*(2*math.pi)/360)
    for y, line in enumerate(screen.chars):
        fgline = screen.fg[y]
        bgline = screen.bg[y]
        ctx.translate(0, font_height)
        #ctx.set_line_width(1); ctx.move_to(0,0.5); ctx.line_to(800, 0.5); ctx.stroke()
        ctx.move_to(0, 0)   # set the current point for show_text and rel_line_to
        ctx.save()
        for x, char in enumerate(line):
            if bgline[x]:
                ctx.set_source_rgb(*bgline[x])
                x_advance = ctx.text_extents(char)[4]
                ctx.rel_line_to(0, descent)
                ctx.rel_line_to(x_advance, 0)
                ctx.rel_line_to(0, -font_height)
                ctx.rel_line_to(-x_advance, 0)
                ctx.fill()
            ctx.set_source_rgb(*(fgline[x] or (1, 1, 1)))
            ctx.show_text(char)
        ctx.restore()
    ctx.restore()

    ctx.save()
    ctx.set_source_rgb(1, 1, 1)
    ctx.translate(0, window.h - descent)
    ctx.new_path()
    ctx.show_text('%.3ffps' % window.clock.get_fps())
    ctx.restore()


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
