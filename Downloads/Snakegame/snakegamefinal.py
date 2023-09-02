import pygame,sys,random
import pygame.rect
from pygame.locals import (KEYDOWN,K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE)
from pygame.math import Vector2
pygame.init()

running = True
"""
Note:
we are dividing the entire screen space into small square grids. Each of those square grid will be treated as a pixel
"""
#CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
cell_size = 40
cell_number = 20
direction = Vector2(1,0) #start with moving to the right
score = 0
f_collision = False
game_state = True
high_score = []


screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake Game')

#images
#fruit image
fruit = pygame.image.load('apple.png').convert_alpha()

#snake images
#head images
head_up = pygame.image.load('head_up.png').convert_alpha()
head_down = pygame.image.load('head_down.png').convert_alpha()
head_right = pygame.image.load('head_right.png').convert_alpha()
head_left = pygame.image.load('head_left.png').convert_alpha()

#body images
body_vertical = pygame.image.load('body_vertical.png').convert_alpha()
body_horizontal = pygame.image.load('body_horizontal.png').convert_alpha()

body_tr = pygame.image.load('body_tr.png').convert_alpha()
body_tl = pygame.image.load('body_tl.png').convert_alpha()
body_bl = pygame.image.load('body_bl.png').convert_alpha()
body_br = pygame.image.load('body_br.png').convert_alpha()

#tail images
tail_up = pygame.image.load('tail_up.png').convert_alpha()
tail_down = pygame.image.load('tail_down.png').convert_alpha()
tail_left = pygame.image.load('tail_left.png').convert_alpha()
tail_right = pygame.image.load('tail_right.png').convert_alpha()

#font
score_font = pygame.font.Font('PoetsenOne-Regular.ttf',25)

#sound
eating_sound = pygame.mixer.Sound('Sound_crunch.wav')
game_sound = pygame.mixer.Sound('Snake Game - Theme Song.mp3')

#event for the snake to move continuously
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,100)
MUSIC_UPDATE = pygame.USEREVENT + 1




#random fruit coordinates
x = random.randint(0, cell_number - 1)
y = random.randint(0, cell_number - 1)

def create_fruit(x, y):
    pos = Vector2(x, y)
    fruit_rect = pygame.Rect(pos.x * cell_size, pos.y * cell_size, cell_size, cell_size)
    #pygame.draw.rect(screen, (126, 166, 140), fruit_rect)
    screen.blit(fruit, fruit_rect)


snake_body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
initial_snake_body = snake_body[: ]

#vector subtraction of two consecutive blocks gives the direction in which the given block is pointing
def head_pos():
    if snake_body[-2] - snake_body[-1] == Vector2(0,-1):
        return head_down
    if snake_body[-2] - snake_body[-1] == Vector2(0, 1):
        return head_up
    if snake_body[-2] - snake_body[-1] == Vector2(1, 0):
        return head_left
    if snake_body[-2] - snake_body[-1] == Vector2(-1, 0):
        return head_right

def tail_pos():
    if snake_body[1] - snake_body[0] == Vector2(0,-1):
        return tail_down
    if snake_body[1] - snake_body[0] == Vector2(0, 1):
        return tail_up
    if snake_body[1] - snake_body[0] == Vector2(1, 0):
        return tail_left
    if snake_body[1] - snake_body[0] == Vector2(-1, 0):
        return tail_right

def create_snake(snake_body):
    for index,body in enumerate(snake_body):
        snake_rect = pygame.Rect(body.x*cell_size,body.y*cell_size,cell_size,cell_size)
        head = head_pos()
        tail = tail_pos()
        if index == len(snake_body) - 1:
            screen.blit(head,snake_rect)
        elif index == 0:
            screen.blit(tail,snake_rect)
        else:
            #Three blocks and their relation are checked
            prev_body = snake_body[index-1]
            next_body = snake_body[index+1]

            #For horizontal body
            if prev_body.y == next_body.y:
                screen.blit(body_horizontal,snake_rect)
            #For vertical body
            elif prev_body.x == next_body.x:
                screen.blit(body_vertical,snake_rect)
            #When the body turns
            else:
                #Top Left or Left Top turn
                if prev_body.y - body.y == 1 and next_body.x - body.x == -1:
                    screen.blit(body_bl,snake_rect) #bl has tl image
                elif prev_body.x - body.x == 1 and next_body.y - body.y == -1:
                    screen.blit(body_tr,snake_rect)
                #Top Right or Right Top turn
                elif prev_body.y - body.y == 1 and next_body.x - body.x== 1:
                    screen.blit(body_br,snake_rect) #br has tr image
                elif prev_body.x - body.x == -1 and next_body.y - body.y == -1:
                    screen.blit(body_tl,snake_rect)
                #Bottom Left or Left Bottom turn
                elif prev_body.y - body.y == -1 and next_body.x - body.x == -1:
                    screen.blit(body_tl,snake_rect) #tl has bl image
                elif prev_body.x - body.x == 1 and next_body.y - body.y == 1:
                    screen.blit(body_br,snake_rect)
                #Bottom Right or Right Bottom turn
                else:
                    if prev_body.x - body.x == -1 and next_body.y - body.y == 1:
                        screen.blit(body_bl,snake_rect)
                    else:
                        screen.blit(body_tr,snake_rect)



def move_snake(body,direction):
    body_clone = body[:]
    for i in range(len(body_clone)-1):
        body_clone[i] = body_clone[i+1]
    body_clone[-1] = body_clone[-1]+direction
    body = body_clone[:]
    return body

#functions for handling collisions
#positive collisions
def pos_collision_detect():
    global score,snake_body
    x_c,y_c = x,y
    f_pos = Vector2(x,y)
    if f_pos in snake_body:
        score += 1
        eating_sound.play()
        x_c = random.randint(0,cell_number-1)
        y_c = random.randint(0,cell_number-1)
        if direction.y != 0:
            body_clone = snake_body[:]
            body_clone.insert(0,snake_body[0]+Vector2(0,1))
            snake_body = body_clone[:]
        if direction.x != 0:
            body_clone = snake_body[:]
            body_clone.insert(0,snake_body[0] + Vector2(-1,0))
            snake_body = body_clone[:]
    return x_c,y_c

#negative collisions
def neg_collision_detect():
    #snake hitting the walls
    snake_head = snake_body[-1]
    if not (0 <= snake_head.x < cell_number) or not (0 <= snake_head.y < cell_number):
        return True
    #snake hitting itself
    for body in snake_body[:-1]:
        if body == snake_head:
            return True
    return False

#for grass pattern
def create_grass():
    lcolour = (167,209,61)
    rcolour = (175,215,70)
    for i in range(cell_number) :
        for j in range(cell_size):
            grass_rect = pygame.Rect(i*cell_size, j*cell_size, cell_size, cell_size)
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(screen,lcolour,grass_rect)
                else:
                    pygame.draw.rect(screen,rcolour,grass_rect)
            else:
                if j % 2 == 0:
                    pygame.draw.rect(screen,rcolour,grass_rect)
                else:
                    pygame.draw.rect(screen,lcolour,grass_rect)

#creating score text
def draw_score():
    global score
    score_text = str(score)
    score_surface = score_font.render(score_text,True, (56,74,12))
    x_pos = cell_size*cell_number - 50
    y_pos = cell_size*cell_number - 50
    score_rect = score_surface.get_rect(center = (x_pos,y_pos))
    fr_rect = fruit.get_rect(midright = (score_rect.left,score_rect.centery))
    screen.blit(score_surface,score_rect)
    screen.blit(fruit,fr_rect)

#handling gameover screen

gameover_state = False
def gameover():
    screen.fill((0,0,0))
    gameover_font = pygame.font.SysFont('Arial', 72)
    gameover_surface = gameover_font.render('GAME OVER', True, (255, 255, 255))
    gameover_rect = gameover_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    screen.blit(gameover_surface, gameover_rect)
    pygame.display.update()
c = 0
while running:
    if game_state:
        pygame.time.set_timer(MUSIC_UPDATE, 28000)
        game_state = False
    #gameloop

    def gameloop():
        global c,snake_body,direction,score,gameover_state,game_state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == SCREEN_UPDATE:
                snake_body = move_snake(snake_body,direction)
            if c == 0:
                game_sound.play()
                c = 1
            if event.type == MUSIC_UPDATE:
                game_sound.play()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    sys.exit()
                if event.key == K_UP:
                    if direction.y != 1:
                        direction = Vector2(0, -1)
                        snake_body = move_snake(snake_body,direction)
                if event.key == K_DOWN:
                    if direction.y != -1:
                        direction = Vector2(0, 1)
                        snake_body = move_snake(snake_body,direction)
                if event.key == K_LEFT:
                    if direction.x != 1:
                        direction = Vector2(-1, 0)
                        snake_body = move_snake(snake_body,direction)
                if event.key == K_RIGHT:
                    if direction.x != -1:
                        direction = Vector2(1, 0)
                        snake_body = move_snake(snake_body,direction)
            if neg_collision_detect():
                direction = Vector2(0,0)
                snake_body = initial_snake_body[:]
                gameover_state = True
                game_sound.stop()
                game_state = True
                high_score.append(score)
                c = 0
                score = 0
    if gameover_state:
        gameover()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                gameover_state = False
    else:
        gameloop()
        create_grass()
        create_snake(snake_body)
        draw_score()
        x,y = pos_collision_detect()
        create_fruit(x, y)
        pygame.display.update()



    clock.tick(60)  # framerate