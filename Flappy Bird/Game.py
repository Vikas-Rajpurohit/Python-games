import pygame
import sys
from pygame.locals import *
import random

# Intializing Game
pygame.init()
clock = pygame.time.Clock()
fps = 60
flying = False
game_over = False
pass_pipe = False
score = 0

# Parameters
screen_w = 800
screen_h = 600
font = pygame.font.SysFont('Bauhaus 93',60)
white = (255,255,255)
ground_scroll = 0
scroll_speed = 4
pipe_gap = 150 
pipe_frequency = 1500 # Milli-Seconds
last_pipe = pygame.time.get_ticks()

# Loading Images
bg = pygame.image.load('Sprites/background.png')
ground_img = pygame.image.load('Sprites/ground.png')
img1 = pygame.image.load('Sprites/bird1.png')
img2 = pygame.image.load('Sprites/bird2.png')
img3 = pygame.image.load('Sprites/bird3.png')
button_img = pygame.image.load('Sprites/restart.png')

def text_screen(text,font,color,x,y):
    screen_text = font.render(text,True,color)
    screen.blit(screen_text,[x,y])

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_h/2)
    score = 0
    return score # Or declare it as global

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
                #########
        self.images = [img1,img2,img3]
        self.index = 0
        self.counter = 0
        # for num in range (1,4):
        #     img = pygame.image.load(f'Sprites/bird{num}.png')
        #     self.images.append(img)

        # self.image = pygame.image.load('Sprites/bird1.png')
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.Clicked = False

    def update(self):
        if flying == True:
            # Adding gravity
            self.vel += 0.2
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 500:
                self.rect.y += int(self.vel)

        if game_over == False:
            # Jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.Clicked == False:
                self.Clicked = True
                self.vel = -5
            if keys[pygame.K_SPACE] == 0:
                self.Clicked = False

            # To Handle Animation
            self.counter +=1
            flap_cooldown = 5 # Higher the Num Slow Flapping Speed

            if(self.counter > flap_cooldown):
                self.counter = 0
                self.index += 1
                if(self.index >= len(self.images)):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotating the bird
            self.image = pygame.transform.rotate(self.images[self.index], -2*self.vel)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/pipe.png')
        self.rect = self.image.get_rect()
        # Position 1 is from Top, -1 is from Bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True) # Image and Which axis ?
            self.rect.bottomleft = [x,y-int(pipe_gap)/2]
        if position == -1:
            self.rect.topleft = [x,y+int(pipe_gap)/2]

    def update(self):
        self.rect.x -= scroll_speed
        if(self.rect.x < -60):
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

bird_group = pygame.sprite.Group() # Keep Track-Motion of Bird
pipe_group = pygame.sprite.Group() # Keep Track-Motion of Pipe

flappy = Bird(100,int(screen_h / 2))
bird_group.add(flappy)

button = Button(screen_w // 2-50,screen_h // 2-100, button_img)

# Screen Window
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('Flappy Bird')

# Continuous Loop
run = True 
while run:
    clock.tick(fps)

    screen.blit(bg,(0,0)) # Background

    # Bird 
    bird_group.draw(screen)
    bird_group.update()
    # Pipe 
    pipe_group.draw(screen)

    # Check the Score
    if len(pipe_group) > 0:
        if (bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left) and (bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right) and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    text_screen(str(score),font,white,int(screen_w/2),20)

    # Look for Collision
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top < 0:
        # If we want to Kill any group
        game_over = True

    # Check if bird has hit the ground
    if flappy.rect.bottom >= 500:
        game_over = True
        flying =  False

    # Draw & Scroll The Ground
    screen.blit(ground_img,(ground_scroll,500))

    if game_over == False and flying == True:
        # Generating New Pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_ht = random.randint(-150,150)
            btm_pipe = Pipe(screen_w,int(screen_h/ 2)+pipe_ht,-1)
            top_pipe = Pipe(screen_w,int(screen_h/ 2)+pipe_ht, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    # Check for Game-Over and Reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) and flying == False and game_over == False:
            flying = True

    pygame.display.update()    

pygame.quit()
sys.exit()