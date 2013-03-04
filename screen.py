
class Screen(object):
    def __init__(self):
        mainfg = (0.7, 0.7, 0.7)
        self.mainbg = (0, 0, 0)
        self.chars = [[u' '] * 80 for i in xrange(25)]
        self.fg = [[mainfg] * 80 for i in xrange(25)]
        self.bg = [[None] * 80 for i in xrange(25)]

    def write(self, x, y, s):
        for i, c in enumerate(s):
            self.chars[y][x+i] = c

    def recolor(self, xfrom, xto, y, fg, bg):
        for x in xrange(xfrom, xto):
            self.fg[y][x] = fg
            self.bg[y][x] = bg
