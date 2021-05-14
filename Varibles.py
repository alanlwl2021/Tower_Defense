import pygame as pg
from os import path

pg.init()

WIDTH, HEIGHT = 1500, 750
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

TILESIZE = 50

vec = pg.math.Vector2

fonts = {}

file = path.join('Data', 'PixelFont.ttf')
for i in range(1, 350):
    fonts[i] = pg.font.Font(file, i)

bvar = {}
bvar['Quad'] = {}
bvar['Quad']['Damage'] = [5, 6, 7, 8, 9, 10, 10]
bvar['Quad']['Reload'] = [40, 35, 30, 25, 20, 15, 15]
bvar['Quad']['Speed'] = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.25]

bvar['Line'] = {}
bvar['Line']['Damage'] = [3, 3.5, 4, 4.5, 5, 5.5, 5.5]
bvar['Line']['Reload'] = [15, 13, 11, 9, 7, 5, 5]
bvar['Line']['Speed'] = [2, 2.5, 3, 3.5, 4, 4.5, 4.5]

bvar['Twin'] = {}
bvar['Twin']['Damage'] = [3, 3.5, 4, 4.5, 5, 5.5, 5.5]
bvar['Twin']['Reload'] = [7.5, 6.5, 5.5, 4.5, 3.5, 2.5, 2.5]
bvar['Twin']['Speed'] = [2, 2.5, 3, 3.5, 4, 4.5, 4.5]

bvar['Flank'] = {}
bvar['Flank']['Damage'] = [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.5]
bvar['Flank']['Reload'] = [9, 8, 7, 6, 5, 4, 3, 3]
bvar['Flank']['Speed'] = [2, 2.75, 3.5, 4.25, 5, 5.75, 5.75]

bvar['Slow'] = {}
bvar['Slow']['Damage'] = [0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.25]
bvar['Slow']['Reload'] = [0, 0]
bvar['Slow']['Speed'] = [0, 0]

bvar['Trap'] = {}
bvar['Trap']['Damage'] = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 100]
bvar['Trap']['Reload'] = [0, 0]
bvar['Trap']['Speed'] = [0, 0]

intro_img = pg.image.load(path.join('Data/Images', 'Intro.png'))
intro_img = pg.transform.smoothscale(intro_img, (WIDTH, HEIGHT)).convert()
