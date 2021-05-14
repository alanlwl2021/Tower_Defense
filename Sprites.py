import pygame as pg
import Global as gl
from Varibles import *
from Functions import *
import random

class Enemy(pg.sprite.Sprite):
    def __init__(self, type):
        pg.sprite.Sprite.__init__(self, gl.enemys)
        self.type = type

        if self.type == 'Basic':
            self.radius = TILESIZE * 0.5 - 5
            self.color = (255, 255, 0)
            self.speed = 2
            self.health = 20
            self.dmg = 2
            self.price = 10

        elif self.type == 'Fast':
            self.radius = TILESIZE * 0.5 - 5
            self.color = (100, 100, 255)
            self.speed = 4
            self.health = 10
            self.dmg = 3
            self.price = 15

        elif self.type == 'Strong':
            self.radius = TILESIZE * 0.5 - 5
            self.color = (255, 100, 0)
            self.speed = 1
            self.health = 40
            self.dmg = 4
            self.price = 20

        self.health *= 1 + gl.wave * 0.75
        self.dmg *= 1 + gl.wave * 0.75
        self.price *= 1 + gl.wave * 0

        self.image = pg.Surface((self.radius * 2, self.radius * 2)).convert()
        self.rect = self.image.get_rect(center=gl.map['Spawner'])
        self.point = 1
        self.group = 'Enemy'

        self.mhealth = self.health
        self.ospeed = self.speed

        self.pos = [self.rect.centerx, self.rect.centery]

    def update(self):

        if self.health <= 0:
            self.kill()
            gl.money += self.price

        self.move()
        self.draw()

    def move(self):
        target = gl.map['Points'][self.point]

        angle = round(point_at(self.pos, target) / 90) * 90

        self.speed = self.ospeed
        for t in gl.towers:
            if self.rect.colliderect(t.rect):
                if t.type == 'Slow':
                    if self.ospeed * t.bullet['Damage'] < self.speed:
                        self.speed *= t.bullet['Damage']
                elif t.type == 'Trap':
                    self.health -= t.bullet['Damage'] * 0.1

        vel = vec(self.speed, 0).rotate(-angle)

        self.pos[0] += vel[0]
        self.pos[1] += vel[1]

        dis = get_dis(self.pos, target)
        if dis <= self.speed * 0.5 + 0.1:
            self.pos = target
            self.pos = [target[0], target[1]]
            if self.point >= gl.map['PointLength'] - 1:
                self.health = 0
                gl.lives -= 1
            else:
                self.point += 1

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def draw(self):
        if self.health <= 0:
            self.health = 0

        color = [self.color[0], self.color[1], self.color[2]]

        for i in range(3):
            minus = color[i]
            rate = (self.mhealth - self.health) / self.mhealth * minus

            color[i] -= rate
            color[i] = round(color[i])

        color = (color[0], color[1], color[2])


        pg.draw.circle(screen, color, (self.rect.centerx + 375, self.rect.centery), self.radius)

class Tower(pg.sprite.Sprite):
    def __init__(self, x, y, point, type):
        pg.sprite.Sprite.__init__(self, gl.towers)
        self.size = TILESIZE - 10
        self.point = point
        self.type = type
        self.group = 'Tower'

        gl.map['Spots'][point[0], point[1]] = self


        self.fire = 0
        self.mfire = 0

        self.bullet = {}

        if self.type == 'Line':
            self.bullet['Radius'] = 5
            self.color = (150, 0, 150)

        if self.type == 'Twin':
            self.bullet['Radius'] = 5
            self.color = (0, 0, 150)

        if self.type == 'Quad':
            self.bullet['Radius'] = 7
            self.color = (255, 0, 255)

        if self.type == 'Flank':
            self.bullet['Radius'] = 4
            self.color = (150, 150, 0)

        if self.type == 'Slow':
            self.bullet['Radius'] = 0
            self.color = (150, 150, 150)
            self.size = 30

        if self.type == 'Trap':
            self.bullet['Radius'] = 0
            self.color = (255, 100, 0)
            self.size = 30

        self.bullet['Damage'] = 0
        self.bullet['Speed'] = 0

        self.upgrades = [0, 0, 0]
        self.angle = 90

        self.image = pg.Surface((self.size, self.size)).convert()
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center = (x, y))

        self.shootvar = 0

    def update(self):

        if self.rect.collidepoint((pg.mouse.get_pos()[0] - 375, pg.mouse.get_pos()[1])) and gl.mouse_down:
            gl.clicking = self

        if gl.clicking == self:
            if gl.keydown[pg.K_a]:
                self.angle += 90
            if gl.keydown[pg.K_d]:
                self.angle -= 90


        self.bullet['Damage'] = bvar[self.type]['Damage'][self.upgrades[0]]
        self.mfire = bvar[self.type]['Reload'][self.upgrades[1]]
        self.bullet['Speed'] = bvar[self.type]['Speed'][self.upgrades[2]]

        self.gun()
        self.draw()

    def gun(self):
        self.fire -= 1
        if self.fire <= 0:
            self.fire = self.mfire
            self.shoot()

    def shoot(self):
        if self.type == 'Line':
            center = vec(self.rect.centerx - 5, self.rect.centery - 5) + vec(self.size * 0.5, 0).rotate(-self.angle)
            Bullet(center, self, self.angle, self.bullet['Speed'], self.bullet['Radius'], self.bullet['Damage'])

        if self.type == 'Twin':
            self.shootvar += 1
            self.shootvar %= 2
            for i in range(2):
                if self.shootvar == i:
                    center = vec(self.rect.centerx - 5, self.rect.centery - 5) + vec(self.size * 0.5, (i - 0.5) * self.size * 0.5).rotate(-self.angle)
                    Bullet(center, self, self.angle, self.bullet['Speed'], self.bullet['Radius'], self.bullet['Damage'])

        if self.type == 'Quad':
            for i in range(4):
                center = vec(self.rect.centerx - 7, self.rect.centery - 7) + vec(self.size * 0.65, 0).rotate(- (45 + i * 90))
                Bullet(center, self, 45 + i * 90, self.bullet['Speed'], self.bullet['Radius'], self.bullet['Damage'])

        if self.type == 'Flank':
            for i in range(2):
                center = vec(self.rect.centerx - 4, self.rect.centery - 4) + vec(self.size * 0.5, 0).rotate(- (i * 180 + self.angle))
                Bullet(center, self, i * 180 + self.angle, self.bullet['Speed'], self.bullet['Radius'], self.bullet['Damage'])

    def draw(self):
        screen.blit(self.image, (self.rect.x + 375, self.rect.y))

    def draw_info(self):

        name_sur = fonts[40].render(self.type + ' Tower', False, self.color)

        temp_sur = pg.Surface((WIDTH * 0.25, HEIGHT)).convert()
        temp_sur.fill((25, 0, 20))

        temp_sur.blit(pg.transform.scale2x(self.image), (WIDTH * 0.125 - self.size, 50))
        temp_sur.blit(name_sur, (WIDTH * 0.125 - name_sur.get_width() * 0.5, 150))


        if self.type in ['Line', 'Quad', 'Twin', 'Flank']:
            colorlist = [[(255, 0, 0), (100, 0, 0), (175, 0, 0)], [(255, 255, 0), (100, 100, 0), (175, 175, 0)], [(0, 255, 0), (0, 100, 0), (0, 175, 0)]]

            varibles = [['Damage', '{:.2f}'.format(self.bullet['Damage']), '{:.2f}'.format(bvar[self.type]['Damage'][self.upgrades[0]+1]), 'Damage'],
            ['Reload', '{:.2f}s/b'.format(self.mfire / 60), '{:.2f}s/b'.format(bvar[self.type]['Reload'][self.upgrades[1]+1] / 60), 'Reload'],
            ['Bullet Speed', '{:.2f}m/s'.format(self.bullet['Speed']), '{:.2f}m/s'.format(bvar[self.type]['Speed'][self.upgrades[2]+1]), 'Speed']]

            num = 3

            price = [100, 100, 100]

        elif self.type == 'Slow':
            colorlist = [[(0, 255, 255), (0, 100, 100), (0, 175, 175)]]
            varibles = [['Effect', 'x{:.2f}'.format(self.bullet['Damage']), 'x{:.2f}'.format(bvar[self.type]['Damage'][self.upgrades[0]+1]), 'Damage']]

            num = 1
            price = [200]

        elif self.type == 'Trap':
            colorlist = [[(255, 0, 255), (100, 0, 100), (175, 0, 175)]]
            varibles = [['Damage', '{:.2f}'.format(self.bullet['Damage']), '{:.2f}'.format(bvar[self.type]['Damage'][self.upgrades[0]+1]), 'Damage']]

            num = 1
            price = [80]

        for i in range(num):
            sur1 = fonts[30].render(varibles[i][0], False, colorlist[i][0])
            sur2 = fonts[30].render(varibles[i][1], False, colorlist[i][1])
            sur3 = fonts[30].render('>', False, (255, 255, 255))
            sur4 = fonts[30].render(varibles[i][2], False, colorlist[i][2])
            sur5 = fonts[20].render('Upgrade', False, (0, 255, 255))
            if self.upgrades[i] < len(bvar[self.type][varibles[i][3]]) - 2:
                sur6 = fonts[20].render('$' + str(price[i]), False, (0, 0, 255))
            else:
                sur6 = fonts[20].render('MAX', False, (255, 0, 0))
            temp_sur.blit(sur1, (WIDTH * 0.125 - sur1.get_width() * 0.5, 250 + i * 160))
            temp_sur.blit(sur2, (30, 300 + i * 160))
            temp_sur.blit(sur3, (WIDTH * 0.125 - sur3.get_width() * 0.5, 300 + i * 160))

            sur7 = pg.Surface((WIDTH * 0.25 - 60, 40)).convert()
            sur7.fill((0, 50, 50))
            if sur7.get_rect(topleft = (30, 345 + i * 160)).collidepoint((pg.mouse.get_pos()[0] - WIDTH * 0.75, pg.mouse.get_pos()[1])) and gl.gameon:
                sur7.fill((0, 100, 100))
                if gl.mouse_down and self.upgrades[i] < len(bvar[self.type][varibles[i][3]]) - 2 and gl.money >= price[i]:
                    gl.money -= price[i]
                    self.upgrades[i] += 1

            temp_sur.blit(sur7, (30, 345 + i * 160))
            temp_sur.blit(sur4, (WIDTH * 0.25 - 30 - sur4.get_width(), 300 + i * 160))
            temp_sur.blit(sur5, (50, 350 + i * 160))
            temp_sur.blit(sur6, (WIDTH * 0.25 - 50 - sur6.get_width(), 350 + i * 160))



        return temp_sur

class Bullet(pg.sprite.Sprite):
    def __init__(self, cen, owner, angle, speed, radius, dmg):
        pg.sprite.Sprite.__init__(self, gl.bullets)
        self.owner = owner
        self.angle = angle
        self.speed = speed
        self.radius = radius
        self.color = (0, 0, 0)
        self.image = pg.Surface((self.radius * 2, self.radius * 2)).convert()
        self.rect = self.image.get_rect(center = cen)
        self.speed = speed

        self.time = 30
        self.health = 1
        self.dmg = dmg

        self.pos = [self.rect.centerx, self.rect.centery]
        self.group = 'Bullet'

    def update(self):
        self.time -= 1
        if self.time <= 0 or self.health <= 0:
            self.kill()
        self.move()
        self.collide()
        self.draw()

    def collide(self):
        for enemy in gl.enemys:
            if get_dis(self.rect.center, enemy.rect.center) <= self.radius + enemy.radius:
                self.health -= enemy.dmg
                enemy.health -= self.dmg

    def move(self):
        vel = vec(self.speed, 0).rotate(-self.angle)

        self.pos[0] += vel[0]
        self.pos[1] += vel[1]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self):
        pg.draw.circle(screen, self.color, (self.rect.centerx + 375, self.rect.centery), self.radius)

class Spawner(pg.sprite.Sprite):
    def __init__(self):
        self.wave = 0
        self.time = 0
        self.mtime = 90
        self.team = [0, 0, 30, 'Basic']
        self.spawnsleft = 0
        self.wavetype = 1
        self.var = 0

    def update(self):
        if self.team[0] > 0:
            self.team[1] -= 1
            if self.team[1] <= 0:
                self.team[1] = self.team[2]
                self.team[0] -= 1
                if self.spawnsleft > 0:
                    self.spawn()
                    self.spawnsleft -= 1
                else:
                    gl.wave += 1
                    self.team[0] = 0
                    self.newwave()
        else:
            self.time -= 1
            if self.time <= 0:
                self.time = self.mtime
                if self.wavetype == 1:
                    self.team = [5, 0, 20, 'Basic']
                elif self.wavetype == 2:
                    self.var += 1
                    self.var %= 2
                    if self.var == 0:
                        self.team = [5, 0, 10, 'Fast']
                    else:
                        self.team = [5, 0, 20, 'Basic']
                elif self.wavetype == 3:
                    self.team = [3, 0, 40, 'Strong']

                elif self.wavetype == 4:
                    self.var += 1
                    self.var %= 3
                    if self.var == 0:
                        self.team = [5, 0, 10, 'Fast']
                    elif self.var == 1:
                        self.team = [5, 0, 20, 'Basic']
                    else:
                        self.team = [3, 0, 40, 'Strong']
                elif self.wavetype == 5:
                    self.team = [30, 0, 10, 'Fast']
                elif self.wavetype == 6:
                    self.team = [15, 0, 20, 'Basic']
                elif self.wavetype == 7:
                    self.team = [10, 0, 40, 'Strong']

                elif self.wavetype == 8:
                    self.var += 1
                    self.var %= 3
                    if self.var == 0:
                        self.team = [10, 0, 10, 'Fast']
                    elif self.var == 1:
                        self.team = [7, 0, 20, 'Basic']
                    else:
                        self.team = [5, 0, 40, 'Strong']

    def newwave(self):
        if gl.wave <= 2:
            self.wavetype = 1
        elif gl.wave <= 4:
            self.wavetype = 2
        elif gl.wave == 5:
            self.wavetype = random.randint(1, 2)
        elif gl.wave <= 7:
            self.wavetype = 3
        elif gl.wave <= 9:
            self.wavetype = random.randint(1, 3)
        elif gl.wave == 10:
            self.wavetype = 4
        elif gl.wave <= 15:
            self.wavetype = 5
        elif gl.wave <= 17:
            self.wavetype = 6
        elif gl.wave <= 19:
            self.wavetype = 7
        elif gl.wave <= 25:
            self.wavetype = random.randint(5, 8)
        else:
            self.wavetype = random.randint(5, 8)

        if self.wavetype == 1:
            self.var = 0
            self.spawnsleft = 15

        elif self.wavetype == 2:
            self.var = 0
            self.spawnsleft = 25

        elif self.wavetype == 3:
            self.var = 0
            self.spawnsleft = 9

        elif self.wavetype == 4:
            self.var = 0
            self.spawnsleft = 15

        elif self.wavetype == 5:
            self.var = 0
            self.spawnsleft = 30

        elif self.wavetype == 6:
            self.var = 0
            self.spawnsleft = 15

        elif self.wavetype == 7:
            self.var = 0
            self.spawnsleft = 10

        elif self.wavetype == 8:
            self.var = 0
            self.spawnsleft = 22


    def spawn(self):
        Enemy(self.team[3])
