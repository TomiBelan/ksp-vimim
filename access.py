#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division

import os
import sys
import time
import json
import copy
import random


class Access(dict):
    def __init__(self, pid):
        dict.__init__(self)
        self.path = '/proc/%s/fd/0' % pid
        self.loaded = {}
        self.load()

    def load(self):
        with open('state') as f:
            self.loaded = json.load(f)
        self.clear()
        self.update(copy.deepcopy(self.loaded))

    def senddata(self, content):
        with open(self.path, 'w') as f:
            f.write(json.dumps(content))

    def save(self):
        tosend = {}
        for k in self:
            if self[k] != self.loaded.get(k):
                tosend[k] = self[k]
        self.senddata(tosend)
        self.loaded = copy.deepcopy(self)


def getpid():
    return os.popen('pgrep -nf "python.*vimim"', 'r').read().strip()


def connect():
    pid = getpid()
    if not pid: raise OSError('vimim process not found')
    return Access(pid)
