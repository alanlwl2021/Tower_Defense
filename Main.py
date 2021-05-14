import pygame as pg
import Global as gl
from Varibles import *
from Sprites import *
from Functions import *

pg.init()

spawner = Spawner()

gl.clicking = None
#Tower(175, 125, [3, 2], 'Line')
#Tower(225, 125, [4, 2], 'Quad')

while gl.intro:
    clock.tick(60)
    text = 'Tower Defense - {:.2f} FPS'.format(clock.get_fps())
    pg.display.set_caption(text)

    gl.mouse_down = False
    gl.right_down = False

    gl.keydown = {}
    for i in [pg.K_ESCAPE, pg.K_a, pg.K_d, pg.K_RETURN, pg.K_SPACE]:
        gl.keydown[i] = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            gl.run = False
            gl.intro = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                gl.mouse_down = True

            if event.button == 3:
                gl.right_down = True

        if event.type == pg.KEYDOWN:
            if event.key in gl.keydown:
                gl.keydown[event.key] = True


    screen.blit(intro_img, (0, 0))
    sur = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
    sur.set_alpha(150)
    screen.blit(sur, (0, 0))


    if gl.introtab == 'Main':
        title = fonts[100].render('Tower Defense', False, (255, 255, 255))
        version = fonts[50].render('v1.1', False, (255, 0, 255))
        version = pg.transform.rotate(version, 30)

        screen.blit(title, (WIDTH * 0.5 - title.get_width() * 0.5, 75))
        screen.blit(version, (WIDTH * 0.5 + title.get_width() * 0.5 - 50, 125))

        texts = ['PLAY', 'CONTROLS', 'EXIT', 'CREDITS']
        colors = [(0, 255, 0), (255, 255, 0), (255, 0, 0), (0, 0, 255)]
        hovercolors = [(150, 255, 150), (255, 255, 150), (255, 150, 150), (150, 150, 255)]
        for i in range(4):
            label = fonts[60].render(texts[i], False, colors[i])
            tl = (WIDTH * 0.5 - label.get_width() * 0.5, 300 + i * 100)
            if label.get_rect(topleft = tl).collidepoint(pg.mouse.get_pos()):
                label = fonts[80].render(texts[i], False, hovercolors[i])
                tl = (WIDTH * 0.5 - label.get_width() * 0.5, 290 + i * 100)
                if gl.mouse_down:
                    if texts[i] == 'PLAY':
                        gl.intro = False
                    elif texts[i] == 'CONTROLS':
                        gl.introtab = 'Controls'
                    elif texts[i] == 'EXIT':
                        gl.run = False
                        gl.intro = False
                    elif texts[i] == 'CREDITS':
                        gl.introtab = 'Credits'

            screen.blit(label, tl)

    elif gl.introtab == 'Controls':
        for i in range(1):
            label = fonts[60].render('BACK', False, (150, 150, 150))
            tl = (WIDTH * 0.5 - label.get_width() * 0.5, 600)

            if label.get_rect(topleft = tl).collidepoint(pg.mouse.get_pos()):
                label = fonts[80].render('BACK', False, (255, 255, 255))
                tl = (WIDTH * 0.5 - label.get_width() * 0.5, 590)

                if gl.mouse_down:
                    gl.introtab = 'Main'

            screen.blit(label, tl)

        label = fonts[100].render('CONTROLS', False, (255, 255, 0))
        screen.blit(label, (WIDTH * 0.5 - label.get_width() * 0.5, 50))

        texts = ['Click a tower for extra informations.', 'Spawing and upgrading towers requires money.', 'Rotate a tower with A / D after clicking it.', 'You have {} lives and lose 1 everytime an enemy reaches the end.'.format(gl.lives),
        'You lost when you have no lives left.', 'Each wave gets harder and harder.']
        for i in range(len(texts)):
            c = round(255 - round(i / len(texts) * 255) * 0.5)
            label = fonts[35].render(texts[i], False, (c, c, c))
            label2 = fonts[35].render(texts[i], False, (0, 0, 0))
            screen.blit(label2, (WIDTH * 0.5 - label.get_width() * 0.5 + 3, 250 + i * 50 + 3))
            screen.blit(label, (WIDTH * 0.5 - label.get_width() * 0.5, 250 + i * 50))


    elif gl.introtab == 'Credits':
        for i in range(1):
            label = fonts[60].render('BACK', False, (150, 150, 150))
            tl = (WIDTH * 0.5 - label.get_width() * 0.5, 600)

            if label.get_rect(topleft = tl).collidepoint(pg.mouse.get_pos()):
                label = fonts[80].render('BACK', False, (255, 255, 255))
                tl = (WIDTH * 0.5 - label.get_width() * 0.5, 590)

                if gl.mouse_down:
                    gl.introtab = 'Main'

            screen.blit(label, tl)

        label = fonts[100].render('CREDITS', False, (0, 0, 255))
        screen.blit(label, (WIDTH * 0.5 - label.get_width() * 0.5, 50))

        texts = ['Made by : Anonymous', 'Made using : Python 3.8 + Pygame + Tiled', 'Font used : Minecraft', 'Images drawn using : Pygame 3.8 + Pixilart', 'Song used : --NA--']
        for i in range(len(texts)):
            c = round(255 - round(i / len(texts) * 255) * 0.5)
            label = fonts[35].render(texts[i], False, (c, c, c))
            label2 = fonts[35].render(texts[i], False, (0, 0, 0))
            screen.blit(label2, (WIDTH * 0.5 - label.get_width() * 0.5 + 3, 250 + i * 50 + 3))
            screen.blit(label, (WIDTH * 0.5 - label.get_width() * 0.5, 250 + i * 50))

    pg.display.update()


while gl.run:
    clock.tick(60)
    text = 'Tower Defense - {:.2f} FPS'.format(clock.get_fps())
    pg.display.set_caption(text)

    gl.mouse_down = False
    gl.right_down = False

    gl.keydown = {}
    for i in [pg.K_ESCAPE, pg.K_a, pg.K_d, pg.K_RETURN, pg.K_SPACE]:
        gl.keydown[i] = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            gl.run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                gl.mouse_down = True
            if event.button == 3:
                gl.clicking = None
                gl.right_down = True
        if event.type == pg.KEYDOWN:
            if event.key in gl.keydown:
                gl.keydown[event.key] = True

    if gl.keydown[pg.K_SPACE]:
        gl.gameon = not gl.gameon
        if gl.gameover or gl.lives <= 0:
            gl.gameover = False
            gl.lives = 100
            gl.wave = 0
            gl.startspawn = False
            gl.money = 1000

            for t in gl.towers:
                t.kill()
            for e in gl.enemys:
                e.kill()
            for b in gl.bullets:
                b.kill()

    if gl.gameon:
        if gl.placing != None:
            gl.clicking = None

        if gl.keydown[pg.K_RETURN]:
            gl.startspawn = True

    screen.fill((0, 150, 0))

    screen.blit(gl.GAMEMAP, (WIDTH * 0.5 - 375, 0))

    if gl.gameon:
        if gl.startspawn:
            spawner.update()
        gl.towers.update()
        gl.enemys.update()
        gl.bullets.update()

    else:
        for t in gl.towers:
            t.draw()
        for e in gl.enemys:
            e.draw()
        for b in gl.bullets:
            b.draw()

    screen.blit(draw_side(), (0, 0))

    if gl.placing != None:
        size = 30
        sur = pg.Surface((size, size)).convert_alpha()
        sur.set_alpha(150)

        if gl.gameon:
            pos = pg.mouse.get_pos()
            gl.mousep = pos
        else:
            pos = gl.mousep
        pos = [pos[0] - 375 - 25, pos[1] - 25]
        pos[0] = round(pos[0] / 50) * 50 + 25
        pos[1] = round(pos[1] / 50) * 50 + 25

        color = (0, 255, 0)

        acp = pg.mouse.get_pos()[0]
        if acp > 375 and acp < WIDTH - 375:
            spot = [pos[0] / 50 - 0.5, pos[1] / 50 - 0.5]
            spot = [round(spot[0]), round(spot[1])]
            if gl.placing in ['Line', 'Quad', 'Twin', 'Flank']:
                num = 0
            else:
                num = 1
            if gl.map['Spots'][spot[0], spot[1]] != num:
                color = (255, 0, 0)
        else:
            color = (255, 0, 0)


        if acp <= 375 or acp >= WIDTH - 375:
            color = (255, 0, 0)

        sur.fill(color)

        screen.blit(sur, (pos[0] + 375 - size * 0.5, pos[1] - size * 0.5))

        if color == (0, 255, 0):
            if gl.mouse_down and gl.gameon:
                Tower(pos[0], pos[1], spot, gl.placing)
                gl.placing = None

        if gl.right_down and gl.placing != None:
            gl.money += {'Line' : 75, 'Quad' : 150, 'Twin' : 250, 'Flank' : 300, 'Slow' : 400, 'Trap' : 500}[gl.placing]
            gl.placing = None


    elif gl.clicking != None:
        if gl.clicking.group == 'Tower':
            pg.draw.circle(screen, (125, 0, 255), (gl.clicking.rect.centerx + 375, gl.clicking.rect.centery), gl.clicking.size, 10)
            sur = gl.clicking.draw_info()
            screen.blit(sur, (WIDTH * 0.75, 0))


    if not gl.startspawn:
        presstext = fonts[25].render('Press ENTER to start', False, (255, 255, 255))
        screen.blit(presstext, (WIDTH * 0.125 - presstext.get_width() * 0.5, 350))

    if not gl.gameon:
        sur = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
        sur.set_alpha(150)
        screen.blit(sur, (0, 0))

        if not gl.gameover:

            texts = ['PAUSED', 'Press SPACE to resume.']
            if not gl.gamestart:
                texts = ['READY', 'Press SPACE to start.']

            pausetext = fonts[200].render(texts[0], False, (255, 255, 255))
            pressspacetext = fonts[50].render(texts[1], False, (255, 255, 255))
            exittext = fonts[50].render('Press ESC to quit.', False, (255, 0, 0))
            screen.blit(pausetext, (WIDTH * 0.5 - pausetext.get_width() * 0.5, 150))
            screen.blit(pressspacetext, (WIDTH * 0.5 - pressspacetext.get_width() * 0.5, 450))
            screen.blit(exittext, (WIDTH * 0.5 - exittext.get_width() * 0.5, 600))

            if pg.key.get_pressed()[pg.K_ESCAPE]:
                gl.run = False

        else:
            exittext = fonts[30].render('Press ESC to quit.', False, (255, 0, 0))
            screen.blit(exittext, (WIDTH * 0.5 - exittext.get_width() * 0.5, 650))
            pausetext = fonts[150].render('GAME OVER', False, (255, 0, 0))
            pressspacetext = fonts[30].render('Press SPACE to start again.', False, (255, 255, 255))
            wavetext = fonts[50].render('You lost at WAVE ' + str(gl.wave), False, (255, 255, 0))

            if gl.wave >= gl.highscore:
                recordtext = fonts[50].render('NEW RECORD!', False, (0, 255, 0))
                gl.highscore = gl.wave
            else:
                recordtext = fonts[50].render('Best WAVE : ' + str(gl.highscore), False, (0, 255, 255))

            screen.blit(pausetext, (WIDTH * 0.5 - pausetext.get_width() * 0.5, 75))
            screen.blit(pressspacetext, (WIDTH * 0.5 - pressspacetext.get_width() * 0.5, 600))
            screen.blit(wavetext, (WIDTH * 0.5 - wavetext.get_width() * 0.5, 350))
            screen.blit(recordtext, (WIDTH * 0.5 - recordtext.get_width() * 0.5, 425))


            if pg.key.get_pressed()[pg.K_ESCAPE]:
                gl.run = False

    else:
        if not gl.gamestart:
            gl.gamestart = True

    if gl.lives <= 0:
        gl.lives = 0
        gl.gameon = False
        gl.gamestart = False
        gl.gameover = True

    pg.display.update()

pg.quit()

with open(path.join('Data', 'Highscore.txt'), 'w') as f:
    try:
        f.write(str(gl.highscore))
    except:
        pass
