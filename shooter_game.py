
from typing import Any
from pygame import *
from random import randint
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

score = 0
lost = 0
goal = 10
max_lost = 3
live = 3
rel_time = False

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "galaxy.jpg" 
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, 620), -40, 80,50, randint(1,3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(5):
    asteroid = Enemy(img_enemy, randint(80, 620), -40, 80,50, randint(1,3))
    asteroids.add(asteroid)

bullets = sprite.Group()


font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('Ты победил!', True, (255,255,255))
lose = font1.render('Ты проиграл (', True, (255,255,255))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Стрелялка")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
        
    if not finish:
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезарядка', 1, (150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False
        
        
        window.blit(background,(0,0))
        ship.update()
        ship.reset()
        
        text = font2.render('Счет: ' + str(score), 1,(255,255,255))
        window.blit(text,(10,20))
        text_lost = font2.render('Пропустил:  ' + str(lost), 1,(255,255,255))
        window.blit(text_lost,(10,50))
        
        monsters.update()
        monsters.draw(window)

        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)

        collides =sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, 620), -40, 80,50, randint(1,3))
            monsters.add(monster)
        
        if score >= goal:
            finish = True
            window.blit(win, (200,200))

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            live -= 1

        if live == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))
        if live == 3:
            life_color = (0,150,0)
        if live == 2:
            life_color = (150,150,0)
        if live == 1:
            life_color = (150,0,0)

        text_life = font1.render(str(live), 1, life_color)
        window.blit(text_life, (650,10))

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroid:
            a.kill()
        time.delay(3000)
        for i in range (5):
            monster = Enemy(img_enemy, randint(80, 620), -40, 80,50, randint(1,3))
            monsters.add(monster)
        for i in range (3):
            asteroid = Enemy(img_enemy, randint(80, 670), -40, 80,50, randint(1,5))
            asteroids.add(asteroid)

       
    display.update()
    clock.tick(FPS)
   
