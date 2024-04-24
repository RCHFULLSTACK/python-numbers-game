import pygame
import os
from game import Game

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set up screen and constant definitions
screen_width = 600
screen_height = 500
# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("World Of Guessing Numbers! V.1")
# Set up game icon
icon = pygame.image.load("assets/image/icon_image.png")
pygame.display.set_icon(icon)
# Load background music and play continuously
pygame.mixer.music.load("assets/sound/background_music.mp3")
pygame.mixer.music.play(-1)
# Load background image
background_image = pygame.image.load("assets/image/background_image.jpg").convert()
# Load number images
number_images = [pygame.image.load(os.path.join('assets', 'image', f"number_{i}.png")).convert_alpha()
                 for i in range(1, 11)]


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game = Game(self.screen_width, self.screen_height)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.game.handle_events(event)
                self.game.handle_button_clicks(event)

            self.game.draw(self.screen)
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.run()
