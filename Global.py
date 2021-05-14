import pygame as pg
from Varibles import *
import pytmx
from os import path

pg.init()

run = True

map = {}

def load_map(filename, m):
    global map_data, map

    map_data = pytmx.load_pygame(path.join('Data/Maps', filename), pixelalpha=True)

    ti = map_data.get_tile_image_by_gid
    for layer in map_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = ti(gid)
                if tile:
                    image = pg.transform.scale(tile, (TILESIZE, TILESIZE))
                    m.blit(image, (x * TILESIZE, y * TILESIZE))


    for t in map_data.objects:
        if t.name == 'Spawner':
            map['Spawner'] = [t.x + TILESIZE * 0.5, t.y + TILESIZE * 0.5]
        if t.name == 'End':
            map['End'] = [t.x + TILESIZE * 0.5, t.y + TILESIZE * 0.5]

    map['Points'] = {}
    map['Points'][0] = map['Spawner']

    for t in map_data.objects:
        if t.name[0 : 5] == 'Point':
            num = t.name[5 : len(t.name)]
            map['Points'][int(num)] = [t.x + TILESIZE * 0.5, t.y + TILESIZE * 0.5]

    map['Points'][len(map['Points'])] = map['End']
    map['PointLength'] = len(map['Points'])



    mapw, maph = int(map_data.width), int(map_data.height)

    game_map = []
    spots = {}

    for y in range(maph):
        l = []
        for x in range(mapw):
            var = map_data.get_tile_properties(x, y, 0)
            if var != None:
                l.append(var['id'])
            else:
                l.append(None)

            if var['id'] == 6:
                spots[x, y] = 0
            else:
                spots[x, y] = 1

        game_map.append(l)

    map['Tiles'] = game_map
    map['Spots'] = spots
    map['Width'] = mapw
    map['Height'] = maph

    # y = 1
    # for layer in game_map:
    #     x = 1
    #     for tile in layer:
    #         if tile == 6:


    return m


GAMEMAP = pg.Surface((750, 750)).convert()
load_map('Map1.tmx', GAMEMAP)



enemys = pg.sprite.Group()
towers = pg.sprite.Group()
bullets = pg.sprite.Group()

mouse_down = False
right_down = False
clicking = None
placing = None

keydowns = None

money = 1000
wave = 0
lives = 100
startspawn = False
gameon = False

mousep = [0, 0]
intro = True
introtab = 'Main'
gamestart = False
gameover = False


with open(path.join('Data', 'Highscore.txt'), 'r') as f:
    try:
        highscore = int(f.read())
    except:
        highscore = 0
