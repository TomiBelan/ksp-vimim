# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE
import tempfile
import pygame
from screen import Screen

class Submit(object):
    SAVE = ['task', 'ok_credit_gain']

    def __init__(self, vimim):
        self.vimim = vimim
        self.task = 0
        self.ok_credit_gain = 700
        self.process = None
        self.outfile = tempfile.mkstemp()[1]
        for name in self.vimim.task_names:
            if not os.path.isdir('testovac/task_data/'+name):
                raise OSError('zly task name')

    def draw(self, ctx):
        screen = Screen()
        screen.write(0, 0, u"Submitting...")
        if self.vimim.have_status_bar:
            self.vimim.draw_generic_status_bar(screen)
        self.vimim.postprocess_screen(screen)
        self.vimim.window.draw_terminal(self.vimim.window, ctx, screen)

    def keydown(self, event):
        self.vimim.bell()

    def open(self):
        self.vimim.app = self

        current_task = '' if self.task == len(self.vimim.task_names) else self.vimim.task_names[self.task]

        content = u'\n'.join(self.vimim.editor_app.content) + u'\n'
        cleaned = content.replace(u' ', u'').replace(u'\n', u'')
        lang = 'pas' if cleaned.startswith('program') or cleaned.endswith('end.') else 'cpp'
        print ['./testovac/testovac.sh', current_task, lang, self.outfile]
        self.process = Popen(['./testovac/testovac.sh', current_task, lang, self.outfile], stdin=PIPE)
        self.process.stdin.write(content.encode('utf-8'))
        self.process.stdin.close()

    def idle(self):
        if not self.process: return
        # print 'h', self.process.returncode
        if self.process.poll() is None: return
        # print self.process.returncode
        code = self.process.returncode
        if self.process.returncode == 0:
            self.vimim.config_app.credits += self.ok_credit_gain
            self.task += 1
        self.process = None
        with open(self.outfile) as f: output = f.read().decode('utf-8')
        # print self.outfile
        # print output   # DEBUG
        print '---------- begin submit log (status %d) ----------' % code
        print output,
        print '---------- end submit log ----------'
        if self.vimim.features['noresult']:
            self.vimim.app = self.vimim.editor_app
            return
        if self.vimim.features['ide']:
            for i, line in enumerate(output.strip().split('\n')):
                self.vimim.editor_app.content.insert(self.vimim.editor_app.y+1+i, line)
            self.vimim.app = self.vimim.editor_app
            return
        self.vimim.problem_app.open(output)
