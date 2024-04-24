import pygame

from constants import color_inactive, BLACK


class Button:
    def __init__(self, x, y, width, height, text='', color=color_inactive, text_color=BLACK, radius=5, font_size=28,
                 enabled=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.radius = radius
        self.enabled = enabled
        self.font = pygame.font.Font(pygame.font.match_font('arial'), font_size)

    def draw(self, screen):
        if not self.enabled:
            # Draw disabled button with a different color
            disabled_color = (200, 200, 200)
            pygame.draw.rect(screen, disabled_color, self.rect, border_radius=self.radius)
        else:
            # Draw the button with rounded edges
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.radius)
        # Add text to the button
        if self.text != '':
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.enabled:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
