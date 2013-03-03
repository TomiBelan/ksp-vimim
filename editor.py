
from screen import Screen

class Editor(object):
    def __init__(self, vimim):
        self.vimim = vimim
        self.x = 0
        self.y = 0
        self.scroll = 0
        self.content = []
        self.mode = self.insert_mode

    @property
    def height(self):
        return 25   # TODO status bar

    def draw(self, ctx):
        screen = Screen()
        for y, line in enumerate(self.content[self.scroll:self.scroll+self.height]):
            screen.write(0, y, line[0:80])
        if (0 <= self.y - self.scroll < self.height) and (0 <= self.x < 80):
            screen.bg[self.y - self.scroll][self.x] = screen.fg[self.y - self.scroll][self.x]
            screen.fg[self.y - self.scroll][self.x] = screen.mainbg
        # TODO status bar
        self.vimim.window.draw_terminal(self.vimim.window, ctx, screen)

    def keydown(self, event):
        self.mode(event)


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
        self.content[y] = self.content[y].ljust(x)

    def splice(self, y, xfrom, xto, replace=u''):
        self.normalize(y, xto)
        line = self.content[y]
        line = line[:xfrom] + replace + line[xto:]
        self.content[y] = line
        if y != self.y: return
        if xto - xfrom == len(replace): return
        if xfrom < self.x or (xfrom == self.x and xto <= self.x):
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


    # MODY

    def insert_mode(self, event):
        if not event: return
        if event.unicode == u'\n':
            self.newline()
        elif event.unicode == u'\t':
            self.splice(self.y, self.x, self.x, u' ')
        elif event.unicode and ord(event.unicode[0]) >= 32:
            self.splice(self.y, self.x, self.x, event.unicode)

    insert_mode.name = u'INSERT MODE'

