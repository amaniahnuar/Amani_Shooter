from pygame import *
from time import sleep
from random import randint

# create window
win = display.set_mode(size=(700, 500))

# Sound and Music
mixer.init()
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.2)

mixer.music.load("C:/Users/akibi/MUSIC/TWICE - What Is Love (Easy Lyrics).mp3")
mixer.music.set_volume(0.1)
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, x, y, sizex, sizey, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale( image.load(sprite_img), (sizex, sizey) )
        self.x = x
        self.y = y
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def boop(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        # controls
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= 610:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", x=self.rect.centerx, y=self.rect.top, sizex=15, sizey=20, speed=15)
        b_group.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global miss_p
        # falling AI
        self.rect.y += self.speed
        # fall at the bottom of screen
        if self.rect.y > 500:
            self.rect.y = 10
            self.rect.x = randint(0,700)
            miss_p += 1

class Bullet(GameSprite):
    def update(self):
        # bullet travels upwards
        self.rect.y -= self.speed
        # disappear at top screen
        if self.rect.y < 0:
            self.kill()

# Sprite
bg = transform.scale( image.load("galaxy.jpg"), (700,500) )
ship = Player("rocket.png", x=5, y=400, sizex=80, sizey=80, speed=10)
b_group = sprite.Group()
e_group = sprite.Group()
for i in range(1,4):
    e = Enemy("ufo.png", x=randint(0,700), y=10, sizex=80, sizey=80, speed=randint(1,3))
    e_group.add(e)

# Score
score_p = 0
miss_p = 0

font.init()
f = font.Font(None, 40)
vic = f.render("YOU WIN!", True, (255, 255, 255))
lose = f.render("GAME OVER!", True, (180, 0, 0))

# Game Loop
loop = True

while loop:
    # Event.get gives a list of input
    for e in event.get():
        # if one of the input is QUIT ( X-button ), loop ends
        if e.type == QUIT:
            loop = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            fire_sound.play()
            ship.fire()

    # update sprite
    win.blit(bg, (0,0))
    ship.boop()
    ship.update()
    e_group.draw(win)
    e_group.update()
    b_group.draw(win)
    b_group.update()

    # update score
    score = f.render("SCORE: " + str(score_p), 1, (255,255,255))
    win.blit(score, (10,20))
    miss = f.render("MISSED: " + str(miss_p), 1, (255,255,255))
    win.blit(miss, (10,50))

    # CHECK WIN
    # first boolean is to kill e_group, second is to kill b_group [boolean = True/False]
    collides = sprite.groupcollide(e_group, b_group, True, False)
    for c in collides:
        score_p += 1
        # Reset enemy back (go back up)
        e = Enemy("ufo.png", x=randint(0,700), y=10, sizex=80, sizey=80, speed=randint(1,3))
        e_group.add(e)

    if score_p >=30:
        win.blit(vic, (250,250))
        display.update()
        sleep(3)
        loop = False

    # CHECK LOSE
    if miss_p >=10:
    #if miss_p >=10 or sprite.spritecollide(ship, e_group, False):
        win.blit(lose, (250,250))
        display.update()
        sleep(3)
        loop = False

    display.update()