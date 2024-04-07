import pygame
from pygame.locals import *
import random

SCREEN_HEIGHT = 750
SCREEN_WIDTH = 600

class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, type, is_move, chance_moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (width, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_move = is_move
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.falling = False
        self.speed_x = random.randint(1,2)
        self.speed_y = 0
        self.gravity = 0.5
        self.chance_moving = chance_moving
        self.type = type
        self.max_move_counter = random.randint(20, 200)
        self.first_jump = False

    def update(self, scroll):
        # move platform in x-axis
        if self.first_jump == True:
            self.max_move_counter = 2
            self.speed_x = 1
            self.move_counter += 1
            self.rect.x += self.direction * self.speed_x
            self.is_move = 11

        if self.is_move <= self.chance_moving:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed_x
        
        if self.move_counter >= self.max_move_counter or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0
        
        if self.falling == True:
            self.speed_y += self.gravity
            self.rect.y += self.speed_y
            self.is_move = 11
            # self.rect.y += 5

        # move platforms to give illusion of player moving up
        self.rect.y += scroll

        # remove extra platforms
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()