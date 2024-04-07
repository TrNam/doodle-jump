import pygame

class SpriteSheet():
    def __init__(self, image, width, height, scale, color):
        self.sheet = image
        self.width = width
        self.height = height
        self.scale = scale
        self.color = color

    def get_image(self, frame, scale):
        self.scale = scale
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame * self.width), 0, self.width, self.height))
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        image.set_colorkey(self.color)

        return image