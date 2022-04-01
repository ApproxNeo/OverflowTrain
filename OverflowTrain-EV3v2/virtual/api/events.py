import pygame


class Events:
    def __init__(self, display):
        self.display = display
        self.handlers = {}

        self.add_handler(pygame.MOUSEBUTTONDOWN, self.click_event)
        self.add_handler(pygame.QUIT, self.quit_event)

    def run(self, screen):
        for event in pygame.event.get():
            executor = self.handlers.get(event.type)
            if executor:
                executor(event, screen)

    def add_handler(self, event_type, executor):
        self.handlers[event_type] = executor

    def click_event(self, event, screen):
        print(pygame.mouse.get_pos())

    def quit_event(self, event, screen):
        self.display.stop()
