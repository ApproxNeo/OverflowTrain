import pygame
from pygame import Rect
from virtual.api.screen import Screen
from virtual.api.element import Image


class MapScreen(Screen):
    def __init__(self, name):
        super().__init__(name)

        self.add_element(Image(Rect(0, 0, 1000, 1000),
                               pygame.image.load('./virtual/resource/map.jpg')))

        self.train_element = self.add_element(Image(Rect(542, 620, 64, 43.5),
                                                    pygame.image.load('./virtual/resource/train.png')))

    def get_train_element(self):
        return self.train_element
