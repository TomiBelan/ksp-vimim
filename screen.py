
class Screen(object):
    def __init__(self):
        white = (1, 1, 1)
        self.mainbg = (0, 0, 0)
        self.chars = [[u' '] * 80 for i in xrange(25)]
        self.fg = [[white] * 80 for i in xrange(25)]
        self.bg = [[None] * 80 for i in xrange(25)]

    def write(self, x, y, s):
        for i, c in enumerate(s):
            self.chars[y][x+i] = c
