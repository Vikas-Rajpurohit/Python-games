import pygame
import sys
from pygame.locals import *
import time
import random

# Intializing Game
pygame.init()
clock = pygame.time.Clock()
fps = 60
moving = False
game_over = False
pass_stone =  False
score = 0

# Parameters
screen_w = 800
screen_h = 600
font = pygame.font.SysFont('Bauhaus 93',60)
white = (255,255,255)
road_scroll = 0
scroll_speed = 4
stone_frequency = 2000 # Milli-Seconds
last_stone = pygame.time.get_ticks()

# Loading Images
bg = pygame.image.load('Images/Ocean.png')
road = pygame.image.load('Images/Road.png')
stone = pygame.image.load('Images/Stone.png')
car = pygame.image.load('Images/Car.png')
button_img = pygame.image.load('Images/restart.png')

# To display Score
def text_screen(text,font,color,x,y):
    screen_text = font.render(text,True,color)
    screen.blit(screen_text,[x,y])

def music(song):
    print('helo')
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

def reset_game():
    stone_group.empty()
    light.rect.x = 150
    light.rect.y = int(screen_h/2)
    score = 0
    return score # Or declare it as global

# Class Car
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = car
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
    def update(self):
        if game_over == False:
            # Direction
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
            elif keys[pygame.K_RIGHT]:
                self.rect.x += 5
            elif keys[pygame.K_UP]:
                self.rect.y -= 5
            elif keys[pygame.K_DOWN]:
                self.rect.y += 5

# Class Stone
class Stone(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = stone
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        self.rect.x -= scroll_speed
        if(self.rect.right < 0):
            self.kill()

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):

        action = False
        # get Mouse Position
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: # Left Side
                action = True

        # Draw button
        screen.blit(self.image,(self.rect.x,self.rect.y))

        return action

car_group = pygame.sprite.Group() # Keep Track-Motion of Car
stone_group = pygame.sprite.Group() # Keep Track-Motion of Stone

light = Car(150,int(screen_h/2))
car_group.add(light)

button = Button(screen_w // 2-50,screen_h // 2-100, button_img)

# Screem Window
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('Car Rush')

run_once = 1

# Continuous Loop
run = True
music('Sounds/start.mp3')
while run:
    clock.tick(fps)

    screen.blit(bg,(0,0)) # Background

    # Road
    screen.blit(road,(road_scroll,100))

    # Stone
    stone_group.draw(screen)

    # Car
    car_group.draw(screen)
    car_group.update()

    # Check the Score
    if len(stone_group) > 0:
        if (car_group.sprites()[0].rect.left > stone_group.sprites()[0].rect.left) and (car_group.sprites()[0].rect.right < stone_group.sprites()[0].rect.right) and pass_stone == False:
            pass_stone = True
        if pass_stone == True:
            if car_group.sprites()[0].rect.left > stone_group.sprites()[0].rect.right:
                score += 1
                pass_stone = False
    
    text_screen(str(score),font,white,int(screen_w/2),20)

    # Look for Collision
    if pygame.sprite.groupcollide(car_group,stone_group,False,False) or light.rect.left < 0:
        # If we want to Kill any group
        game_over = True

    # Check if Car is on Road
    if (light.rect.bottom > 550) or (light.rect.top < 50):
        game_over = True
        moving = False


    if game_over == False and moving == True:
        # Generating New Stone
        time_now = pygame.time.get_ticks()
        if time_now - last_stone > stone_frequency:
            stone_d = random.randint(0,300)
            obs = Stone(screen_w,(stone_d+100))
            stone_group.add(obs)
            last_stone = time_now

        road_scroll -= scroll_speed
        if abs(road_scroll) > 35:
            road_scroll = 0
        
        stone_group.update()

    # Check for Game-Over and Reset
    if game_over == True:
        if run_once:
            run_once = 0
            music('Sounds/crash.mp3')
        
        if button.draw() == True:
            game_over = False
            run_once = 1
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) and moving == False and game_over == False:
            moving = True

    pygame.display.update()

pygame.quit()
sys.exit()