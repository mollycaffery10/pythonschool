import pygame
import sys
from pygame.locals import *
pygame.init()
 
screen = pygame.display.set_mode((640, 460))
screen.fill((255, 255, 255))
pygame.display.set_caption('Bubble Buster!')
font = pygame.font.SysFont(None, 36)
main_clock = pygame.time.Clock()
#Adds lives to the game
score = 0
lives = 3
alive = True

#set up values for the player
player = pygame.Rect(300, 400, 60, 10)
player_speed = 7

 
move_left = False
move_right = False
 
def draw_screen():
    screen.fill((176,224,230))
def draw_player():
    pygame.draw.rect(screen, (34,139,34), player)

def draw_text(display_string, font, surface, x, y):
    text_display = font.render(display_string, 1, (0, 0, 0))
    text_rect = text_display.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_display, text_rect)
    
def draw_ball():
    ball = pygame.draw.circle(screen, (0, 0, 0), (x_position, y_position), 5, 0)
 
x_position = 320
y_position = 380
last_x = x_position
last_y = y_position
 
ball_can_move = False
speed = [5,-5]
 
#values for  bubbles to use
all_bubbles = []
number_of_bubbles = 30
bubble_radius = 25
bubble_edge = 25
initial_bubble_position = 70
bubble_spacing = 30 #60
 
def create_bubbles():
    bubble_x = initial_bubble_position
    bubble_y = initial_bubble_position
 
    for rows in range(0, 3):
        for columns in range(0, 10):
            bubble = pygame.draw.circle((screen), (0, 0, 0), (bubble_x, bubble_y), bubble_radius, bubble_edge)
            bubble_x += bubble_spacing
            all_bubbles.append(bubble)
        bubble_y += bubble_spacing
        bubble_x = initial_bubble_position
 
create_bubbles()
initial_bubble_position = 200
create_bubbles()
 
def draw_bubbles():
    for bubble in all_bubbles:
        bubble = pygame.draw.circle((screen), (255, 255, 255), (bubble.x, bubble.y), bubble_radius, bubble_edge)
 
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #Keyboard input for players
        if event.type == KEYDOWN:
            if event.key == K_a:
                move_right = False
                move_left = True
            if event.key == K_d:
                move_left = False
                move_right = True
        if event.type == KEYUP:
            if event.key == K_a:
                move_left = False
            if event.key == K_d:
                move_right = False
            if alive:
                if event.key == K_SPACE:
                    ball_can_move = True
            if not alive:
                if event.key == K_RETURN:
                    lives = 3
                    alive = True
                    score = 0
                    ball_can_move = False
                    for x in range(0, len(all_bubbles)):
                        all_bubbles.pop()
                    create_bubbles()
                    
    #Ensure consistent frames per second
    main_clock.tick(50)
 
    #Moves the player
    if move_left and player.left > 0:
        player.x -= player_speed
    if move_right and player.right < 640:
        player.x += player_speed
 
    #Move the ball
    if ball_can_move:
        last_x = x_position
        last_y = y_position
 
        x_position += speed[0]
        y_position += speed[1]
        if ball.x <= 0:
            x_position = 15
            speed[0] = -speed[0]
        elif ball.x >= 640:
            x_position = 625
            speed[0] = -speed[0]
        if ball.y <= 0:
            y_position = 15
            speed[1] = -speed[1]
        #Subtracting lives
        elif ball.y >= 460:
            lives -= 1
            ball_can_move = False
 
        #Test collisions with the player
        if ball.colliderect(player):
            y_position -= 15
            speed[1] = -speed[1]
        #Move direction
        move_direction = ((x_position - last_x), (y_position - last_y))
        print(move_direction)
                #Test collisions with the bubbles
        for bubble in all_bubbles:
            if ball.colliderect(bubble):

                if move_direction[1] > 0:
                    speed[1] = -speed[1]
                    y_position -= 10
                elif move_direction[1] < 0:
                    speed[1] = -speed[1]
                    y_position += 10
                all_bubbles.remove(bubble)
                score += 100
                break
 
    else:
        x_position = player.x + 30
        y_position = 380

    if lives <= 0:
        alive = False
    draw_screen()
    draw_player()
    draw_bubbles()
    ball = pygame.draw.circle(screen, (0, 0, 0), (x_position, y_position), 5, 0)
    if alive:
        draw_text('Score: %s' % (score), font, screen, 5, 5)
        draw_text('Lives: %s' % (lives), font, screen, 540, 5)
    else:
        draw_text('Game Over, sorry......', font, screen, 255, 5)
        draw_text('Press Enter to Play Again', font, screen, 180, 50)
 
    pygame.display.update()
