import math
import pygame as pg
import Global as gl
from Varibles import *

def get_dis(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def lerp(mode, l, tar, rate):
    if mode in ['pos', 'vel']:
        l[0] += (tar[0] - l[0]) * rate
        l[1] += (tar[1] - l[1]) * rate
    if mode in ['angle']:
        ang = ((tar-l) + 180) % 360 - 180
        l += ang * rate

    if mode in ['single']:
        return l + (tar - l) * rate
    if mode in ['vel']:
        return l[0], l[1]
    if mode in ['angle']:
        return l

def point_at(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    ang = 360 - math.atan2(y2 - y1, x2 - x1) * 180 / math.pi

    return ang

def draw_side():

    pos = pg.mouse.get_pos()

    sur = pg.Surface((375, 750)).convert()
    sur.fill((0, 150, 0))

    wavetext = fonts[60].render('Wave ' + str(gl.wave), False, (255, 150, 150))
    moneytext = fonts[40].render('$' + str(gl.money), False, (200, 200, 0))
    livestext = fonts[50].render(str(gl.lives) + ' Lives', False, (200, 255, 200))
    sur.blit(wavetext, (375 * 0.5 - wavetext.get_width() * 0.5, 50))
    sur.blit(moneytext, (375 * 0.5 - moneytext.get_width() * 0.5, 150))
    sur.blit(livestext, (375 * 0.5 - livestext.get_width() * 0.5, 200))

    colors = [(150, 0, 150), (255, 0, 255), (0, 0, 150), (150, 150, 0), (150, 150, 150), (255, 100, 0)]
    blackcolors = [(75, 0, 75), (130, 0, 130), (0, 0, 75), (75, 75, 0), (75, 75, 75), (130, 50, 0)]

    if gl.gameon:
        colorsclick = [(150, 85, 150), (255, 150, 255), (85, 85, 150), (200, 200, 0), (200, 200, 200), (255, 175, 100)]
    else:
        colorsclick = colors
    towers = ['Line', 'Quad', 'Twin', 'Flank', 'Slow', 'Trap']
    tarwave = [0, 0, 5, 10, 15, 25]

    price = [75, 150, 250, 300, 400, 500]

    for i in range(6):

        tsur = pg.Surface((75, 75)).convert()
        tsur.fill(colors[i])

        if i >= 3:
            y = 1
        else:
            y = 0
        cen = (375 * 0.5 - 37.5 + (i % 3 - 1) * 100, 450 + y * 125)
        rect = tsur.get_rect(topleft = cen)

        if not gl.wave >= tarwave[i]:
            tsur.fill(blackcolors[i])

        elif rect.collidepoint(pos[0], pos[1]):
            tsur.fill(colorsclick[i])

            if gl.mouse_down and gl.money >= price[i] and gl.gameon:
                gl.money -= price[i]
                gl.placing = towers[i]

        sur.blit(tsur, cen)
        text = fonts[25].render('$' + str(price[i]), False, (255, 255, 255))
        sur.blit(text, (cen[0] + 75 * 0.5 - text.get_width() * 0.5, 530 + y * 125))

        if not gl.wave >= tarwave[i]:
            wavenum = fonts[30].render(str(tarwave[i]), False, (100, 100, 100))
            sur.blit(wavenum, (cen[0] + 37.5 - wavenum.get_width() * 0.5, (450 + y * 125 + 37.5) - wavenum.get_height() * 0.5))

    return sur
