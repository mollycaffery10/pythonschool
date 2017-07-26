import pygame
import sys
from pygame.locals import *


class BubbleGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 460))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption('Bubble Buster!')
        self.font = pygame.font.SysFont(None, 36)
        self.main_clock = pygame.time.Clock()
        # Adds lives to the game
        self.score = 0
        self.lives = 3
        self.alive = True

        # set up values for the player
        self.player = pygame.Rect(300, 400, 60, 10)
        self.player_speed = 7

        self.move_left = False
        self.move_right = False

        self.x_position = 320
        self.y_position = 380
        self.last_x = self.x_position
        self.last_y = self.y_position

        self.ball_can_move = False
        self.speed = [5, -5]

        self.all_bubbles = []
        # values for  bubbles to use
        self.bubble_config = {'number_of_bubbles': 30,
                              'bubble_radius': 25,
                              'bubble_edge': 25,
                              'initial_bubble_position': 70,
                              'bubble_spacing': 30
                              }

    def runGame(self):
        self.create_bubbles()
        self.bubble_config['initial_bubble_position'] = 200
        self.create_bubbles()
        while True:
            # check for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # Keyboard input for players
                if event.type == KEYDOWN:
                    if event.key == K_a:
                        self.move_right = False
                        self.move_left = True
                    if event.key == K_d:
                        self.move_left = False
                        self.move_right = True
                if event.type == KEYUP:
                    if event.key == K_a:
                        self.move_left = False
                    if event.key == K_d:
                        self.move_right = False
                    if self.alive:
                        if event.key == K_SPACE:
                            self.ball_can_move = True
                    if not self.alive:
                        if event.key == K_RETURN:
                            self.lives = 3
                            self.alive = True
                            self.score = 0
                            self.ball_can_move = False
                            for x in range(0, len(self.all_bubbles)):
                                self.all_bubbles.pop()
                            self.create_bubbles()

            # Ensure consistent frames per second
            self.main_clock.tick(50)

            # Moves the player
            if self.move_left and self.player.left > 0:
                self.player.x -= self.player_speed
            if self.move_right and self.player.right < 640:
                self.player.x += self.player_speed

            # Move the ball
            if self.ball_can_move:
                self.last_x = self.x_position
                self.last_y = self.y_position

                self.x_position += self.speed[0]
                self.y_position += self.speed[1]
                if self.ball.x <= 0:
                    self.x_position = 15
                    self.speed[0] = -self.speed[0]
                elif self.ball.x >= 640:
                    self.x_position = 625
                    self.speed[0] = -self.speed[0]
                if self.ball.y <= 0:
                    self.y_position = 15
                    self.speed[1] = -self.speed[1]
                # Subtracting lives
                elif self.ball.y >= 460:
                    self.lives -= 1
                    self.ball_can_move = False

                # Test collisions with the player
                if self.ball.colliderect(self.player):
                    self.y_position -= 15
                    self.speed[1] = -self.speed[1]
                # Move direction
                self.move_direction = ((self.x_position - self.last_x), (self.y_position - self.last_y))
                # Test collisions with the bubbles
                for bubble in self.all_bubbles:
                    if self.ball.colliderect(bubble):

                        if self.move_direction[1] > 0:
                            self.speed[1] = -self.speed[1]
                            self.y_position -= 10
                        elif self.move_direction[1] < 0:
                            self.speed[1] = -self.speed[1]
                            self.y_position += 10
                            self.all_bubbles.remove(bubble)
                        self.score += 100
                        break

            else:
                self.x_position = self.player.x + 30
                self.y_position = 380

            if self.lives <= 0:
                alive = False
            self.draw_screen()
            self.draw_player()
            self.draw_bubbles()
            self.ball = pygame.draw.circle(self.screen, (0, 0, 0), (self.x_position, self.y_position), 5, 0)
            if self.alive:
                self.draw_text('Score: %s' % (self.score), self.font, self.screen, 5, 5)
                self.draw_text('Lives: %s' % (self.lives), self.font, self.screen, 540, 5)
            else:
                self.draw_text('Game Over, sorry......', self.font, self.screen, 255, 5)
                self.draw_text('Press Enter to Play Again', self.font, self.screen, 180, 50)

            pygame.display.update()

    def draw_screen(self):
        self.screen.fill((176, 224, 230))

    def draw_player(self):
        pygame.draw.rect(self.screen, (34, 139, 34), self.player)

    def draw_text(self, display_string, font, surface, x, y):
        self.text_display = font.render(display_string, 1, (0, 0, 0))
        self.text_rect = self.text_display.get_rect()
        self.text_rect.topleft = (x, y)
        surface.blit(self.text_display, self.text_rect)

    def draw_ball(self):
        self.ball = pygame.draw.circle(self.screen, (0, 0, 0), (self.x_position, self.y_position), 5, 0)

    def create_bubbles(self):
        bubble_x = self.bubble_config['initial_bubble_position']
        bubble_y = self.bubble_config['initial_bubble_position']

        for rows in range(0, 3):
            for columns in range(0, 10):
                bubble = pygame.draw.circle((self.screen), (0, 0, 0), (bubble_x, bubble_y), self.bubble_config['bubble_radius'],
                                            self.bubble_config['bubble_edge'])
                bubble_x += self.bubble_config['bubble_spacing']
                self.all_bubbles.append(bubble)
            bubble_y += self.bubble_config['bubble_spacing']
            bubble_x = self.bubble_config['initial_bubble_position']

    def draw_bubbles(self):
        for bubble in self.all_bubbles:
            bubble = pygame.draw.circle(self.screen, (255, 255, 255), (bubble.x, bubble.y),
                                        self.bubble_config['bubble_radius'], self.bubble_config['bubble_edge'])


bubbleGame = BubbleGame()
bubbleGame.runGame()
