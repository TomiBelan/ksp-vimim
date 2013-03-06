# -*- coding: utf-8 -*-

import pygame
from screen import Screen

class Config(object):
    SAVE = ['features']

    def __init__(self, vimim):
        self.vimim = vimim
        self.focus = 0

        self.features = dict((fid, False) for fid in feature_list)
        self.features['highlight'] = True
        self.features['large'] = True
        self.features['noresult'] = True
        self.features['parens'] = True

    def open(self):
        self.vimim.app = self
        self.focus = 0

    def draw(self, ctx):
        screen = Screen()

        for i, fid in enumerate(feature_list):
            fg = (0, 1, 0) if self.features[fid] else (1, 0, 0)
            bg = (0, 0.3, 0) if i == self.focus else None
            screen.write(0, i+1, u'[X]' if self.features[fid] else u'[ ]')
            screen.recolor(0, 4, i+1, (1, 1, 1), bg)
            screen.write(4, i+1, feature_names[fid])
            screen.recolor(4, 80, i+1, fg, bg)

        desc_y = 3 + len(feature_list)
        selfid = feature_list[self.focus]
        screen.write(4, desc_y-1, feature_names[selfid] + u':')
        for i, row in enumerate(feature_descs[selfid].split(u'\n')):
            screen.write(0, desc_y+i, row)

        bottom = 23 if self.vimim.have_status_bar else 24
        screen.write(0, bottom, u'Z: Zapnúť')
        screen.write(20, bottom, u'V: Vypnúť')   # TODO cena
        screen.write(60, bottom, u'C: Config zavrieť')
        for i in xrange(4):
            screen.recolor(20*i, 20*i+1, bottom, (1, 1, 0), None)

        if self.vimim.have_status_bar:
            self.vimim.draw_generic_status_bar(screen)
            screen.write(0, 24, u'-- CONFIG MODE --')
        self.vimim.postprocess_screen(screen)
        self.vimim.window.draw_terminal(self.vimim.window, ctx, screen)

    def keydown(self, event):
        if event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
            self.vimim.bell()
            return

        selfid = feature_list[self.focus]
        if event.key == pygame.K_z and not self.features[selfid]:
            self.features[selfid] = True
        elif event.key == pygame.K_v and self.features[selfid]:
            # TODO pay
            self.features[selfid] = False
        elif event.key == pygame.K_UP or event.key == pygame.K_e:
            self.focus -= 1
            if self.focus < 0: self.focus += len(feature_list)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_x:
            self.focus += 1
            if self.focus == len(feature_list): self.focus = 0
        elif event.key == pygame.K_c:
            self.vimim.app = self.vimim.editor_app
        else:
            self.vimim.bell()

    def idle(self):
        self.vimim.game_app.idle()



feature_defs = u'''

highlight
Farebné zvýrazňovanie
    Mýlia sa vám 0 s O, 1 s l, a podobne? Iné editory vám možno ponúkajú
    zvýrazňovanie čísel atď. inou farbou, ale Vimim dokáže zvýrazňovať
    nielen čísla, ale úplne všetko.

large
Pomoc pre zrakovo postihnutých
    Nevidíte na obrazovku? Nevadí. Vimim môže písmená zobrazovať väčšie.

japan
Japonské písanie textu
    Písanie znakov japonským spôsobom. Samozrejme, funguje to aj s latinkou.

green
Pokojná zelená
    Ste v neustálom strese? Vimim vám ponúka ukľudňujúce zelené pozadie.
    Ale aby ste neboli kľudní až príliš a nezaspali pri kódení, kompenzuje
    to akčným červeným písmom.

parens
Dopĺňanie zátvoriek a úvodzoviek
    Automaticky doplní zatvárajúce párové znaky - zátvorky, úvodzovky a
    podobne.

noresult
Šetrič nervov
    Tlie vám program? Vytáča vás kompilátor? Stále hádže WA? Šetrite si vaše
    nervy a zapnite si túto fičúriu.

rot13
ROT13 šifrovanie
    Striehnu vám za ramenom mraky ľudí, pripravení odkukať vám vo chvíľke
    nepozornosti vaše heslá, alebo (glg!) vaše intelektuálne vlastníctvo?
    Zašifrujte váš editor rokmi overenou šifrou ROT13 a zmaríte ich temné
    plány! (Pozor, písmená s diakritikou zostanú nezašifrované.)

nostatus
Plná obrazovka
    Status bar sa vypne, aby ste sa mohli plne sústrediť na editovaný text a
    videli z neho čo najviac.

horse
Šachový kôň
    Príležitosť vyskúšať nový, rýchlejší spôsob pohybu.

180
Iný pohľad na vec
    Nie a nie nájsť ten bug? Možno pomôže pozrieť sa na to z iného uhla.

double
Zdvojnásobená efektivita
    Chcete za rovnaký čas napísať dvakrát toľko kódu? Vimim vám pomôže
    dosiahnuť tento cieľ a získať si tým obdiv všetkých okolo vás.

spellcheck
Kontrola pravopisu
    Nejde ti spisovná slovenčina? Neboj sa, ak spravíš nejaký preklep alebo
    chybu, Vimim ju za teba opraví.

ide
Integrované debugovanie
    Ak váš program alebo kompilátor vyhodí chybu, Vimim vám ukáže, kde je,
    priamo v editore.

nocursor
Kompaktný kurzor
    Nechcete, aby bol kurzor obdĺžnik? Niektoré editory podporujú aj kurzory
    v tvare úsečky, ale iba Vimim ponúka skutočnú kompaktnosť!

'''
feature_list = []
feature_names = {}
feature_descs = {}
for f in feature_defs.strip().split(u'\n\n'):
    fid, name, desc = f.split(u'\n', 2)
    feature_list.append(fid)
    feature_names[fid] = name
    feature_descs[fid] = desc
