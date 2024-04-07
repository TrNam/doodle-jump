import pygame
from pygame.locals import *

PLAYER_SIZE = (50,50)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
MOVE_SPEED = 8

class Player():
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, PLAYER_SIZE)
        self.rect_w = 35
        self.rect_h = 50
        self.rect = pygame.Rect(x, y, self.rect_w, self.rect_h)
        self.vel_y = 0
        self.flipped = False
        self.hitbox_offset = 16
        self.gravity = 0.2

    def move(self):
        keys = pygame.key.get_pressed()
        
        # movement left right
        if keys[pygame.K_LEFT]:
            self.flipped = False
            self.hitbox_offset = 16
            self.rect.x -= MOVE_SPEED
            if self.rect.left <= -self.rect_w/2:
                self.rect.right = SCREEN_WIDTH + self.rect_w/2
        if keys[pygame.K_RIGHT]:
            self.flipped = True
            self.hitbox_offset = 0
            self.rect.x += MOVE_SPEED
            if self.rect.right >= SCREEN_WIDTH + self.rect_w/2:
                self.rect.left = 0 - self.rect_w/2

        # constantly update gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def grav(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
