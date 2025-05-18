from common_fun import *


class ScorePanel:
    CENTER_VALUE = 105

    # labels
    labels = []

    # text_surfs
    text_surfs = []

    # text_rects
    text_rects = []

    def __init__(self, width, height, my_screen):
        # screen init
        self.screen = my_screen

        # fonts init
        self.font = pygame.font.Font("assets/Fonts/Michroma-Regular.ttf", 30)
        self.font_lower = pygame.font.Font("assets/Fonts/Michroma-Regular.ttf", 15)
        self.font_nums = pygame.font.Font("assets/Fonts/Michroma-Regular.ttf", 20)
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        # offsets
        self.gamer_offset = 0
        self.offsets = [110, 40, 30, 40, 30, 40, 30, 40, 30]
        self.space_between_players = 80

        # szare koło
        self.radius = 1910
        self.circle_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.circle_color = (211, 211, 211, 180)

        # obrazek dante
        self.dante_scale_factor = 0.25
        self.dante_picture = resize_img("assets/imgs/dante.png", int(320 * self.dante_scale_factor),
                                        int(800 * self.dante_scale_factor))

    def append_to_vectors(self, label_text, text_surface, text_rect):
        self.labels.append(label_text)
        self.text_surfs.append(text_surface)
        self.text_rects.append(text_rect)

    def sum_of_offsets(self, end):
        sum_of_offs = 0
        for index in range(0, end):
            sum_of_offs += self.offsets[index]
        return sum_of_offs

    def add_player_components(self, nickname):
        # Gracz id
        label_text = nickname
        text_surface = self.font.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(1)))
        self.append_to_vectors(label_text, text_surface, text_rect)

        # poprawne odpowiedzi
        label_text = "Poprawne odpowiedzi:"
        text_surface = self.font_lower.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(2)))
        self.append_to_vectors(label_text, text_surface, text_rect)

        # poprawne odpowiedzi - liczby
        label_text = "0/0"
        text_surface = self.font_nums.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(3)))
        self.append_to_vectors(label_text, text_surface, text_rect)

        # liczba okrążeń
        label_text = "Liczba okrążeń:"
        text_surface = self.font_lower.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(4)))
        self.append_to_vectors(label_text, text_surface, text_rect)

        # liczba okrążeń - liczby
        label_text = "0/3"
        text_surface = self.font_nums.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(5)))
        self.append_to_vectors(label_text, text_surface, text_rect)

        # prędkość
        label_text = "Prędkość:"
        text_surface = self.font_lower.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(6)))
        self.append_to_vectors(label_text, text_surface, text_rect)

        # prędkość - liczby
        label_text = "0 km/h"
        text_surface = self.font_nums.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(7)))
        self.append_to_vectors(label_text, text_surface, text_rect)

        # boost
        label_text = "Boost:"
        text_surface = self.font_lower.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(8)))
        self.append_to_vectors(label_text, text_surface, text_rect)

        # boost - liczby
        label_text = "Niedostępny"
        text_surface = self.font_nums.render(label_text, True, 'BLACK')
        text_rect = text_surface.get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, self.gamer_offset + self.sum_of_offsets(9)))
        self.append_to_vectors(label_text, text_surface, text_rect)

    def add_components(self):
        # GRACZ 1
        self.add_player_components("Gracz 1")

        # GRACZ 2
        self.gamer_offset += self.sum_of_offsets(9) - self.offsets[0] + self.space_between_players
        self.add_player_components("Gracz 2")

    def blit_panel(self):

        pygame.draw.circle(self.circle_surf, self.circle_color, (self.radius, self.radius), self.radius)

        self.screen.blit(self.circle_surf,
                         (SCREEN_WIDTH / 2 - self.radius + SCREEN_WIDTH + 1040, SCREEN_HEIGHT / 2 - self.radius))
        self.screen.blit(self.dante_picture, (SCREEN_WIDTH - int(800 * self.dante_scale_factor), 0))

        for index in range(0, len(self.labels)):
            self.screen.blit(self.text_surfs[index], self.text_rects[index])
