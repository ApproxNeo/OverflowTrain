import pygame
from pygame import Rect, Surface


class Element:
    def __init__(self, rect: Rect):
        self.rect: Rect = rect

    def render(self, surface):
        pass


class Image(Element):
    def __init__(self, rect: Rect, image: Surface, angle: int = 0):
        super().__init__(rect)
        self.image = image
        self.angle = angle

    def render(self, surface: Surface):
        scaled_img = pygame.transform.smoothscale(self.image,
                                                  (self.rect.height, self.rect.width))

        rotated_img = pygame.transform.rotate(scaled_img, self.angle)
        rotated_rect = rotated_img.get_rect(center=self.rect.center)

        surface.blit(rotated_img, rotated_rect)
