import tkinter as tk
import pygame
import random
import os

from tkinter import filedialog
from button import Button
from constants import WHITE, BLACK, GREEN, RED, color_inactive, color_active, max_input_length, allowed_numbers, \
    screen_width, screen_height


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_guessing_number = pygame.font.Font(pygame.font.match_font('arial'), 48)
        self.font = pygame.font.Font(pygame.font.match_font('arial'), 25)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("World Of Guessing Numbers! V.1")
        pygame.display.set_icon(pygame.image.load(os.path.join("assets", "image", "icon_image.png")))
        self.background_image = pygame.image.load(os.path.join("assets", "image", "background_image.jpg")).convert()
        self.number_images = [pygame.image.load(os.path.join("assets", "image", f"number_{i}.png"))
                              .convert_alpha() for i in range(1, 11)]
        pygame.mixer.music.load(os.path.join("assets", "sound", "background_music.mp3"))
        pygame.mixer.music.play(-1)
        self.secret_number = random.randint(1, 10)
        self.user_input = None
        self.attempts = 0
        self.message = ''
        self.text = ''
        self.message_color = RED
        self.active = False
        self.show_number_image = False
        self.show_rules = False
        self.input_box = pygame.Rect(250, 180, 140, 52)
        self.music_on = True
        self.custom_music_file = None
        self.custom_music_playing = False
        self.check_number_button = None
        self.rules_button = None
        self.restart_button = None
        self.music_button = None
        self.load_button = None
        self.play_stop_button = None
        self.remove_button = None
        self.timer = Timer()
        self.setup_buttons()
        self.reset_game()

    def setup_buttons(self):
        self.check_number_button = Button(200, 250, 200, 80, "Check Number", font_size=28)
        self.rules_button = Button(50, screen_height - 150, 150, 50, "Rules", font_size=20)
        self.restart_button = Button(screen_width // 2 - 75, screen_height - 150, 150, 50,
                                     "Restart", font_size=20)
        self.music_button = Button(screen_width - 200, screen_height - 150, 150, 50,
                                   "Music On/Off", font_size=20)
        self.load_button = Button(50, 420, 150, 50, "Load Music", font_size=20,
                                  color=color_inactive)
        self.play_stop_button = Button(screen_width // 2 - 75, screen_height - 80, 150, 50,
                                       "Play/Stop", font_size=20, color=color_inactive)
        self.remove_button = Button(400, 420, 150, 50, "Remove Music", font_size=20,
                                    color=color_inactive)

    def reset_game(self):
        self.secret_number = random.randint(1, 10)
        self.user_input = None
        self.attempts = 0
        self.message = ''
        self.text = ''
        self.message_color = RED
        self.show_number_image = False
        self.input_box = pygame.Rect(250, 180, 140, 52)
        self.show_rules = False
        self.active = False
        self.custom_music_file = None
        self.custom_music_playing = False
        self.play_stop_button.enabled = False
        self.remove_button.enabled = False
        self.load_button.color = color_active
        self.play_stop_button.color = color_active
        self.remove_button.color = color_active
        self.timer.reset()

    def load_custom_music(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select an MP3 file", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.custom_music_file = file_path
            pygame.mixer.music.load(self.custom_music_file)
            self.custom_music_playing = False
            self.play_stop_button.enabled = True
            self.remove_button.enabled = True
            self.load_button.color = color_active
            self.play_stop_button.color = color_active
            self.remove_button.color = color_active

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if len(self.text) < max_input_length:
                    if event.unicode.isdigit() and event.unicode in allowed_numbers:
                        self.text += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.process_input()

    def process_input(self):
        try:
            self.user_input = int(self.text)
            if self.user_input in range(1, 11):
                self.attempts += 1
                if self.user_input < self.secret_number:
                    self.message = f'Too low! Try again. Attempts: {self.attempts}'
                    self.message_color = RED
                elif self.user_input > self.secret_number:
                    self.message = f'Too high! Try again. Attempts: {self.attempts}'
                    self.message_color = RED
                else:
                    image_index = self.secret_number - 1
                    self.message = f'Correct! You took {self.attempts} attempts'
                    self.message_color = GREEN
                    self.show_number_image = True
            else:
                self.message = 'Please enter a valid number between 1 and 10'
                self.message_color = RED
            self.text = ''
        except ValueError:
            self.message = 'Please enter a valid number'
            self.message_color = RED

    def handle_button_clicks(self, event):
        if self.restart_button.is_pressed(event):
            self.reset_game()
        elif self.check_number_button.is_pressed(event):
            self.process_input()
        elif self.music_button.is_pressed(event):
            self.toggle_music()
        elif self.rules_button.is_pressed(event):
            self.toggle_rules()
        elif self.load_button.is_pressed(event):
            self.load_custom_music()
        elif self.play_stop_button.is_pressed(event) and self.play_stop_button.enabled:
            self.toggle_custom_music()
        elif self.remove_button.is_pressed(event) and self.remove_button.enabled:
            self.remove_custom_music()

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def toggle_rules(self):
        self.show_rules = not self.show_rules

    def toggle_custom_music(self):
        if not self.custom_music_playing:
            print(f"Attempting to play: {self.custom_music_file}")  # Debug statement
            pygame.mixer.music.load(self.custom_music_file)
            pygame.mixer.music.play(-1)
            self.custom_music_playing = True
        else:
            pygame.mixer.music.stop()
            self.custom_music_playing = False

    def remove_custom_music(self):
        self.custom_music_file = None
        self.custom_music_playing = False
        self.play_stop_button.enabled = False
        self.remove_button.enabled = False
        self.load_button.color = color_active
        self.play_stop_button.color = color_active
        self.remove_button.color = color_active

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))

        txt_surface = self.font_guessing_number.render(self.text, True, BLACK)
        width = max(80, txt_surface.get_width() + 10)
        self.input_box.w = width

        pygame.draw.rect(screen, WHITE, self.input_box)
        color = color_active if self.active else color_inactive
        pygame.draw.rect(screen, color, self.input_box, 4)
        screen.blit(txt_surface, (self.input_box.x + 15, self.input_box.y - 2))

        message_surface = self.font.render(self.message, True, self.message_color)
        message_rect = message_surface.get_rect(center=(screen_width // 2, 150))
        screen.blit(message_surface, message_rect)

        if self.show_number_image:
            image_index = self.secret_number - 1
            number_image = self.number_images[image_index]
            image_rect = number_image.get_rect(center=(screen_width // 2, 85))
            screen.blit(number_image, image_rect)

        if self.show_rules:
            self.draw_rules(screen)

        self.restart_button.draw(screen)
        self.check_number_button.draw(screen)
        self.music_button.draw(screen)
        self.rules_button.draw(screen)
        self.load_button.draw(screen)
        self.play_stop_button.draw(screen)
        self.remove_button.draw(screen)
        self.timer.draw(self.screen)

    def draw_rules(self, screen):
        self.font = pygame.font.Font(pygame.font.match_font('arial'), 20)
        rules_text = [
            "Game Rules:",
            "Guess the secret number between",
            "1 and 10 in as few attempts as possible."
        ]
        y = 50
        line_spacing = 30

        for line in rules_text:
            rules_surface = self.font.render(line, True, BLACK)
            rules_rect = rules_surface.get_rect(midtop=(screen_width // 2, y), width=screen_width)
            screen.blit(rules_surface, rules_rect)
            y += line_spacing


class Timer:
    def __init__(self):
        self.font = pygame.font.Font(pygame.font.match_font('arial'), 36)
        self.start_ticks = pygame.time.get_ticks()
        self.reset()

    def reset(self):
        self.start_ticks = pygame.time.get_ticks()

    def draw(self, screen):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        formatted_time = f"{minutes:02}:{seconds:02}"
        timer_surface = self.font.render(formatted_time, True, BLACK)
        timer_rect = timer_surface.get_rect(topleft=(10, 10))
        screen.blit(timer_surface, timer_rect)
