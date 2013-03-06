#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division

import os
import sys
import time
import json
import random
from UserDict import DictMixin


class Access(DictMixin):
    def __init__(self, pid):
        self.last_load = 0
        self.path = '/proc/%s/fd/0' % pid

    def load(self):
        if time.time() < self.last_load + 1: return
        with open('state') as f:
            self.content = json.load(f)
        self.last_load = time.time()

    def send(self, content):
        with open(self.path, 'w') as f:
            f.write(json.dumps(content))

    def __getitem__(self, key):
        self.load()
        return self.content[key]

    def __setitem__(self, key, value):
        self.send({ key: value })

    def __delitem__(self, key):
        raise NotImplementedError()

    def keys(self):
        self.load()
        return self.content.keys()


def getpid():
    return os.popen('pgrep -nf "python.*vimim"', 'r').read().strip()


def connect():
    pid = getpid()
    if not pid: raise OSError('vimim process not found')
    return Access(pid)
