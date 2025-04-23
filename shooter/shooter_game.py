from pygame import *
from random import randint
from time import time as timer
mixer.init()

mixer.music.load('space.ogg')

mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

FPS = 60

window = display.set_mode((700, 500))

score = 0
goal = 10
max_lost = 3
loat = 0
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))


display.set_caption('galaxy')

font.init()

font1 = font.Font(None, 70)

clock = time.Clock()

background = transform.scale(image.load("galaxy.jpg"), (700, 500))


life = 10


class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
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
        bullet = Bullets(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1



class Bullets(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



lost = 0
text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))







win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

#player = Player('rocket.png', 5, win_height - 80, 4)#
#monter = Enemy('ufo.png', 5, win_width - 80, 280)#

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

#sprite1 = transform.scale(image.load('rocket.png'),(100, 100))
#s#prite2 = transform.scale(image.load('ufo.png'), (100, 100))
#wi#ndow.blit(sprite1, (x1, y1))

finish = False

game = True

bullets = sprite.Group()


if life > 0 or  lost >= max_lost:
    finish = True
    window.blit(lose, (200, 200))

font

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    window.blit(background, (0, 0))

    ship.update()
    monster.update()
    bullets.update()
    asteroids.update()

    ship.reset()
    monsters.draw(window)
    bullets.draw(window)
    asteroids.draw(window)

    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
        score = score + 1
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)
    if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
        sprite.spritecollide(ship, monsters, True)
        sprite.spritecollide(ship, asteroids, True)
        life = life -1

#    collides = sprite.groupcollide(asteroid, bullets, True, True)
 #   for c in collides: 
  #      score = score + 1
   #     asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    #    asteroids.add(monster)

        


    if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
        finish = True
        window.blit(lose, (200, 200))

    if score >= goal:
        finish = True
        window.blit(win,(200, 200))
    
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
    display.update()
    clock.tick(FPS)