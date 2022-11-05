# SNAKE GAME...

import pygame
import random

pygame.mixer.init() # To add Music And Jpg
pygame.init() 

# pygame.mixer.music.load("music/back.mp3") # Loading Of Music & Begining
# pygame.mixer.music.play() # To Play Music

# Colors
white = (255,255,255)
green = (0,128,0)
food = (235,195,28)

# Screen Parameters
screen_width = 800
screen_height = 600

# Creating Window
gameWindow = pygame.display.set_mode((screen_width,screen_height)) # Screen Size
pygame.display.set_caption("Snake-bite (*=*)") # Title Of Game
pygame.display.update()

# Background Image
bgimg = pygame.image.load("images/snake.jpg")
bgimg = pygame.transform.scale(bgimg,(800,600)).convert_alpha()
start = pygame.image.load("images/start.jpg")
start = pygame.transform.scale(start,(800,700)).convert_alpha()

clock = pygame.time.Clock() # We have to define our game specific time frame

font = pygame.font.SysFont(None,55) # Font,Size
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,size,size])

def music(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(start,(0,0))
        text_screen("Welcome to Snakes",white,220,100)
        text_screen("-> Press Spacebar to Play <-",white,140,150)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music("music/start.mp3")
                    gameloop()    

        pygame.display.update()
        clock.tick(60)        


# Creating Game Loop => Functioning Of Game...
def gameloop():
    # Game Specific Variables
    exit_game =False
    game_over =False
    snake_x=565 # Position in x from left
    velocity_x=3 # Intial velocity in x
    snake_y=255 # Position in y from above
    velocity_y=0 # Intial Velocity in y
    snake_size=10 # Snake Size
    fps = 30
    score = 0
    snk_list = []
    snk_length =1
    food_x = random.randint(20,screen_width/2)
    food_y = random.randint(20,screen_height/2)

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            gameWindow.blit(start,(0,0))
            text_screen("Game Over !",white,300,150)
            text_screen("Enter to Eat...",white,290,200)
            for event in pygame.event.get():  # Record Every Moment in Display
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()    
        else:
            for event in pygame.event.get():  # Record Every Moment in Display
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN: # This Line mean we Pressed any Key
                    if event.key == pygame.K_s: # CHEAT CODE
                        score += 10
                    if event.key == pygame.K_RIGHT:
                        velocity_x= 3  #=> This will just update on Tap
                        velocity_y= 0
                    if event.key == pygame.K_LEFT:
                        velocity_x= -3  #=> This will just update on Tap
                        velocity_y= 0
                    if event.key == pygame.K_UP:
                        velocity_y= -3  #=> This will just update on Tapx
                        velocity_x= 0
                    if event.key == pygame.K_DOWN:
                        velocity_y= 3  #=> This will just update on Tap 
                        velocity_x= 0     

            snake_x += velocity_x
            snake_y += velocity_y  

            if abs(snake_x-food_x)<10 and abs(snake_y-food_y)<10:
                music("music/score.mp3")
                score +=1
                food_x = random.randint(20,screen_width/2)
                food_y = random.randint(20,screen_height/2)
                snk_length += 5

            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0)) # Image Setup...
            text_screen("Score : "+str(score),green,20,screen_height-60)
            pygame.draw.rect(gameWindow,food,[food_x,food_y,snake_size,snake_size]) 

            head =[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                music("music/game-over.mp3") # Game-over

            if snake_x<0 or snake_y<0 or snake_x>screen_width or snake_y>screen_height:
                game_over =True
                music("music/game-over.mp3")

            plot_snake(gameWindow,white,snk_list,snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()