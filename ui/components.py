import pygame
from ui.colors import *

class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_BLUE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, color=GRAY, handle_color=DARK_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.color = color
        self.handle_color = handle_color
        self.handle_rect = pygame.Rect(x, y, 10, height)
        self.set_value(initial_val)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.handle_color, self.handle_rect)

    def set_value(self, value):
        self.value = value
        pos_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        self.handle_rect.centerx = pos_x

    def get_value(self, pos):
        pos_x = pos[0]
        if self.rect.collidepoint(pos):
            value = (pos_x - self.rect.x) / self.rect.width * (self.max_val - self.min_val) + self.min_val
            self.set_value(max(self.min_val, min(self.max_val, value)))
            return self.value
        return None

class DecisionLog:
    def __init__(self, x, y, width, height, font_size=24, bg_color=WHITE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) * self.font.get_height() > self.rect.height:
            self.messages.pop(0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        for i, msg in enumerate(self.messages):
            text_surface = self.font.render(msg, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5 + i * self.font.get_height()))

class Metrics:
    def __init__(self, x, y, width, height, font_size=24, bg_color=WHITE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.metrics = {}

    def set_metrics(self, metrics):
        self.metrics = metrics

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        i = 0
        for key, value in self.metrics.items():
            text_surface = self.font.render(f"{key}: {value}", True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5 + i * self.font.get_height()))
            i += 1
