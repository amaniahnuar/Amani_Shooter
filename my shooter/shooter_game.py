from pygame import *
from random import randint
from time import sleep

# Create Window
win = display.set_mode(size=(700, 500))

# Music
mixer.init()
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.2)

mixer.music.load("C:/Users/akibi/MUSIC/TWICE - What Is Love (Easy Lyrics).mp3")
mixer.music.set_volume(0.02)
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, sprite_size_x, sprite_size_y, sprite_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(sprite_img), (sprite_size_x, sprite_size_y))
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.sprite_speed = sprite_speed

        # rect properties (for sprite)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = sprite_x, sprite_y
    
    def boop(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 10:
            self.rect.x -= self.sprite_speed
        if keys[K_RIGHT] and self.rect.x <= 600:
            self.rect.x += self.sprite_speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect. top, 15, 20, 15)
        b_group.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global miss_p
        self.rect.y += self.sprite_speed
        # falls over the bottom
        if self.rect.y > 500:
            self.rect.x = randint(0,700)
            self.rect.y = 10
            miss_p += 1

class Bullet(GameSprite):
    def update(self):
        # move bullet upwards
        self.rect.y -= self.sprite_speed
        # disappear when across top screen
        if self.rect.y < 0:
            self.kill()

# Sprites
bg = transform.scale( image.load("galaxy.jpg"), (700, 500))
ship = Player("rocket.png", sprite_x=5, sprite_y=400, sprite_size_x=80, sprite_size_y=80, sprite_speed=10)

e_group = sprite.Group()
for i in range(1,6):
    e = Enemy("ufo.png", sprite_x=randint(0,700), sprite_y=10, sprite_size_x=80, sprite_size_y=80, sprite_speed=randint(1,3))
    e_group.add(e)

b_group = sprite.Group()

# Score
score_p = 0
miss_p = 0

font.init()
f = font.SysFont("Arial", 36)

# Win and Lose
font = font.SysFont("Arial", 80)
vic = font.render("YOU WIN!", True, (255, 255, 255))
lose = font.render("GAME OVER!", True, (180,0,0))

# Game Loop
loop = True

while loop:
    win.blit(bg, (0,0))
    for e in event.get():
        if e.type == QUIT:
            loop = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            fire_sound.play()
            ship.fire()
    
    # For Macs User
    #keys = key.get_pressed()
    #if keys[K_SPACE]:
    #    ship.fire()

    # for ship
    ship.boop()
    ship.update()
    # for enemies
    e_group.draw(win)
    e_group.update()
    # for bullets
    b_group.draw(win)
    b_group.update()

    # for score
    score = f.render("Score: " + str(score_p), 1, (255,255,255))
    win.blit(score, (10,20))
    miss = f.render("Missed: " + str(miss_p), 1, (255,255,255))
    win.blit(miss, (10,50))

    # check for LOSE
    if sprite.spritecollide(ship, e_group, False) or miss_p >= 10:
        win.blit(lose, (200,200))
        display.update()
        sleep(3)
        loop = False

    # check for WIN
    collides = sprite.groupcollide(e_group, b_group, True, True)

    for c in collides:
        score_p += 1
        e = Enemy("ufo.png", sprite_x=randint(0,700), sprite_y=10, sprite_size_x=80, sprite_size_y=80, sprite_speed=randint(5,10)*0.2)
        e_group.add(e)
    
    if score_p >= 30:
        win.blit(vic, (200,200))
        display.update()
        sleep(3)
        loop = False

    display.update()