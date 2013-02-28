
class InsertMode(object):
    def __init__(self, vimim):
        self.vimim = vimim

    def draw(self, ctx):
        self.vimim.editor.draw(ctx)

    def keydown(self, event):
        if event.unicode == u'\n' or event.unicode == u'\r':
            self.vimim.editor.write('\n')
        if event.unicode and ord(event.unicode) >= 32:
            self.vimim.editor.write(event.unicode)
