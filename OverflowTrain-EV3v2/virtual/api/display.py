import pygame
from pygame import Surface
from virtual.api.screen import Screen
from virtual.api.events import Events


class Display:
    def __init__(self, size: tuple):
        self.size = size
        self.screens: dict = {}
        self.window: Surface = None
        self.events: Events = Events(self)
        self.running: bool = False

    def start(self, start_screen: str):
        self.window = pygame.display.set_mode(self.size)
        pygame.init()

        current_screen = self.get_screen(start_screen)
        self.running = True

        while self.running:
            self.events.run(current_screen)
            current_screen.render(self.window)
            pygame.display.update()
            pygame.time.Clock().tick(60)

        pygame.quit()

    def stop(self):
        self.running = False

    def add_screen(self, screen):
        self.screens[screen.name] = screen
        return screen

    def get_screen(self, screen_name: str) -> Screen:
        return self.screens.get(screen_name)
