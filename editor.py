
class Editor(object):
    def __init__(self, window):
        self.window = window
        self.x = 0
        self.y = 0
        self.scroll = 0
        self.content = []
        self.height = 25   # TODO status bar

    def draw(self, ctx):
        chars = self.content[self.scroll:self.scroll+self.height]
        empty_line = [' ' * 80]
        while len(chars) < 25: chars.append(empty_line)
        colors = None
        self.window.draw_terminal(self.window, ctx, chars, colors)

    def move_to(self, nx, ny):
        self.x = max(0, min(79, nx))
        self.y = max(0, ny)
        if self.y < self.scroll:
            self.scroll = self.y
        if self.y > self.scroll + self.height - 1:
            self.scroll = self.y - self.height + 1

    def move_by(self, dx, dy):
        self.move_to(self.x + dx, self.y + dy)

    def write(self, ch):
        if len(ch) > 1:
            for c in ch: self.write(c)
            return

        content = self.content
        while len(content) <= self.y:
            content.append([u' '] * 80)

        if ch == u'\n':
            new_line = content[self.y][self.x:]
            content[self.y] = content[self.y][0:self.x]
            while len(content[self.y]) < 80: content[self.y].append(u' ')
            while len(new_line) < 80: new_line.append(u' ')
            content.insert(self.y + 1, new_line)
            self.move_to(0, self.y + 1)
            return

        if content[self.y][-1] != u' ': return
        content[self.y].pop()
        content[self.y].insert(self.x, ch)

        if self.x == 79:
            self.move_to(0, self.y + 1)
        else:
            self.move_by(1, 0)
