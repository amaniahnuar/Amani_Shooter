from pygame import *
from time import sleep

# SPITE CLASS
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed):
        super().__init__()
        self.img = transform.scale(image.load(img), (50, 50))
        self.speed = speed
        # rect
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.img, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 450:
            self.rect.y += self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        # set direction
        if self.rect.x <=470:
            self.direction = "right"
        if self.rect.x >=650:
            self.direction="left"

        # AI for moving
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, rgb, x, y, width, height):
        self.rgb = rgb
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # drawing wall
        self.img = Surface(size=(self.width, self.height))
        self.img.fill(rgb)
        # rect
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        win.blit(self.img, (self.rect.x, self.rect.y))
        
win = display.set_mode(size=(700, 500))
display.set_caption("Jungle Maze")

# SPRITE
bg = transform.scale(image.load("background.jpg"), (700, 500))
player = Player(img="hero.png", x=5, y=450, speed=5)
enemy = Enemy(img="cyborg.png", x=600, y=350, speed=3)
goal = GameSprite("treasure.png", x=600, y=400, speed=0)

# lose win FONTS
font.init()
font = font.Font(None, 70)
lose = font.render("GAME OVER", True, (180, 0, 0))
victory = font.render("YOU WIN", True, (225, 215, 0))

# Wall
w1 = Wall((154, 205, 50), x=100, y=20, width=450, height=10)
w2 = Wall((154, 205, 50), 100, 480, 350, 10)
w3 = Wall((154, 205, 50), 100, 20 , 10, 380)
w4 = Wall((154, 205, 50), 200, 100 , 10, 380)
w5 = Wall((154, 205, 50), 300, 20 , 10, 380)
w6 = Wall((154, 205, 50), 450, 100 , 10, 390)


# MUSIC
mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.set_volume(0.2)
mixer.music.play()

# GAME LOOP
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    win.blit(bg, (0,0))
    player.update()
    player.reset()

    enemy.update()
    enemy.reset()

    goal.reset()

    w1.draw()
    w2.draw()
    w3.draw()
    w4.draw()
    w5.draw()
    w6.draw()


    # lose check
    if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6):
        win.blit(lose, (200,200))
        sleep(2)
        game = False
    # win check
    if sprite.collide_rect(player, goal):
        win.blit(victory, (200,200))
        sleep(2)
        game = False

    display.update()