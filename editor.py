
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
        empty_line = [u' ' * 80]
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
        content = self.content
        while len(content) <= self.y:
            content.append([u' '] * 80)

        change = content[self.y][:]
        change.insert(self.x, ch)
        change = ''.join(new_line).split('\n')
        change = [line.rstrip(' ').ljust(80) for line in change]
        if any(len(line) > 80 for line in change): return
        content.pop(self.y)
        for i, line in enumerate(change):
            content.insert(self.y + i, list(line))
        if u'\n' in ch:
            self.move_to(len(ch.rpartition(u'\n')[2]), self.y + len(change) - 1)
        else:
            self.move_by(len(ch), 0)
        # TODO ale hento neskoci na novy riadok ked je tento plny
