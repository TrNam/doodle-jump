import pygame
import random

class Bird(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)

        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # determine which side and direction bird is coming from
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        if self.direction == -1:
            self.flip = False

        # add all still images into animation list
        animation_steps = 4
        for step in range(animation_steps):
            image = sprite_sheet.get_image(step, scale)
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey(sprite_sheet.color)
            self.animation_list.append(image)
        
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        
        if self.direction == 1:
            self.rect.right = 0
        elif self.direction == -1:
            self.rect.left = SCREEN_WIDTH
        self.rect.y = y

    def update(self, scroll, SCREEN_WIDTH):

        # animating the bird
        ANIMATION_COOLDOWN = 150
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        # move bird left and right
        self.rect.x += self.direction * 2

        # move bird as player moves
        self.rect.y += scroll

        # mask
        # self.mask = pygame.mask.from_surface(self.image)
        
        # kill bird when off screen
        if (self.direction == 1 and self.rect.left > SCREEN_WIDTH)\
            or (self.rect.right < 0 and self.direction == -1):
            self.kill()
