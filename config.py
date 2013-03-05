# -*- coding: utf-8 -*-

import time
import pygame
import random
from screen import Screen

class Config(object):
    def __init__(self, vimim):
        self.vimim = vimim
        self.focus = 0

    def draw(self, ctx):
        screen = Screen()

        for i, (name, description) in enumerate(feature_texts):
            screen.write(4, i+1, name)
            screen.recolor(0, 80, i+1,
                           (1, 0, 0),
                           (0, 0.3, 0) if i == self.focus else None)

        ydesc = 3 + len(feature_texts)
        screen.write(4, ydesc-1, feature_texts[self.focus][0] + u':')
        for i, row in enumerate(feature_texts[self.focus][1].split(u'\n')):
            screen.write(0, ydesc+i, row)

        if self.vimim.have_status_bar:
            self.vimim.draw_generic_status_bar(screen)
            screen.write(0, 24, u'-- CONFIG MODE --')
        self.vimim.postprocess_screen(screen)
        self.vimim.window.draw_terminal(self.vimim.window, ctx, screen)

    def keydown(self, event):
        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.vimim.bell()
            return

        if event.key == pygame.K_z:
            pass   # TODO
        elif event.key == pygame.K_v:
            pass   # TODO
        elif event.key == pygame.K_UP or event.key == pygame.K_e:
            self.focus -= 1
            if self.focus < 0: self.focus += len(feature_texts)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_x:
            self.focus += 1
            if self.focus == len(feature_texts): self.focus = 0
        elif event.key == pygame.K_c:
            self.vimim.app = self.vimim.editor_app
        else:
            self.vimim.bell()

    def idle(self):
        self.vimim.game_app.idle()



feature_texts = u'''

Farebné zvýrazňovanie
    Mýlia sa vám 0 s O, 1 s l, a podobne? Iné editory vám možno ponúkajú
    zvýrazňovanie čísel atď. inou farbou, ale Vimim dokáže zvýrazňovať
    nielen čísla, ale úplne všetko.

Pomoc pre zrakovo postihnutých
    Nevidíte na obrazovku? Nevadí. Vimim môže písmená zobrazovať väčšie.

Japonské písanie textu
    Písanie znakov japonským spôsobom. Samozrejme, funguje to aj s latinkou.

Pokojná zelená
    Ste v neustálom strese? Vimim vám ponúka ukľudňujúce zelené pozadie.
    Ale aby ste neboli kľudní až príliš a nezaspali pri kódení, kompenzuje
    to akčným červeným písmom.

Dopĺňanie zátvoriek a úvodzoviek
    Automaticky doplní zatvárajúce párové znaky - zátvorky, úvodzovky a
    podobne.

Šetrič nervov
    Tlie vám program? Vytáča vás kompilátor? Stále hádže WA? Šetrite si vaše
    nervy a zapnite si túto fičúriu.

ROT13 šifrovanie
    Striehnu vám za ramenom mraky ľudí, pripravení odkukať vám vo chvíľke
    nepozornosti vaše heslá, alebo (glg!) vaše intelektuálne vlastníctvo?
    Zašifrujte váš editor rokmi overenou šifrou ROT13 a zmaríte ich temné
    plány!

Plná obrazovka
    Status bar sa vypne, aby ste sa mohli plne sústrediť na editovaný text a
    videli z neho čo najviac.

Šachový kôň
    Príležitosť vyskúšať nový, rýchlejší spôsob pohybu.

Iný pohľad na vec
    Nie a nie nájsť ten bug? Možno pomôže pozrieť sa na to z iného uhla.

Zdvojnásobená efektivita
    S touto fičúriou ľahko napíšete dvakrát toľko kódu za rovnaký čas.

Kontrola pravopisu
    Nejde ti spisovná slovenčina? Neboj sa, ak spravíš nejaký preklep alebo
    chybu, Vimim ju za teba opraví.

Integrované debugovanie
    Ak váš program alebo kompilátor vyhodí chybu, Vimim vám ukáže, kde je,
    priamo v editore.

Kompaktný kurzor
    Nechcete, aby bol kurzor obdĺžnik? Niektoré editory podporujú aj kurzory
    v tvare úsečky, ale iba Vimim ponúka skutočnú kompaktnosť!

'''
feature_texts = feature_texts.strip().split(u'\n\n')
feature_texts = [f.split(u'\n', 1) for f in feature_texts]
