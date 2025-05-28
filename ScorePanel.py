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

    # setters
    def set_text(self, string, vectors_index, sum_of_offsets_index, gamer_off):
        self.labels[vectors_index] = string
        self.text_surfs[vectors_index] = self.font_nums.render(self.labels[vectors_index], True, 'BLACK')
        self.text_rects[vectors_index] = self.text_surfs[vectors_index].get_rect(
            midtop=(self.SCREEN_WIDTH - self.CENTER_VALUE, gamer_off + self.sum_of_offsets(sum_of_offsets_index)))

    def set_gamer1_correct_answers(self, string):
        vectors_index = 2
        sum_of_offsets_index = 3
        gamer_off = 0
        self.set_text(string, vectors_index, sum_of_offsets_index, gamer_off)

    def set_gamer2_correct_answers(self, string):
        vectors_index = 11
        sum_of_offsets_index = 3
        gamer_off = self.gamer_offset
        self.set_text(string, vectors_index, sum_of_offsets_index, gamer_off)

    def set_gamer1_loops(self, string):
        vectors_index = 2 + 2
        sum_of_offsets_index = 5
        gamer_off = 0
        self.set_text(string, vectors_index, sum_of_offsets_index, gamer_off)

    def set_gamer2_loops(self, string):
        vectors_index = 11 + 2
        sum_of_offsets_index = 5
        gamer_off = self.gamer_offset
        self.set_text(string, vectors_index, sum_of_offsets_index, gamer_off)

    def set_gamer1_velocity(self, string):
        vectors_index = 2 + 4
        sum_of_offsets_index = 7
        gamer_off = 0
        self.set_text(string, vectors_index, sum_of_offsets_index, gamer_off)

    def set_gamer2_velocity(self, string):
        vectors_index = 11 + 4
        sum_of_offsets_index = 7
        gamer_off = self.gamer_offset
        self.set_text(string, vectors_index, sum_of_offsets_index, gamer_off)

    def set_gamer1_boost(self, string):
        vectors_index = 2 + 6
        sum_of_offsets_index = 9
        gamer_off = 0
        self.set_text(string, vectors_index, sum_of_offsets_index, gamer_off)

    def set_gamer2_boost(self, string):
        vectors_index = 11 + 6
        sum_of_offsets_index = 9
        gamer_off = self.gamer_offset
        self.set_text(string, vectors_index, sum_of_offsets_index, gamer_off)

    # update
    def update_info_player2(self, correct_answers, answers, curr_loop, all_loops, velocity, boosts):
        self.set_gamer2_correct_answers(str(correct_answers) + "/" + str(answers))
        self.set_gamer2_loops(str(curr_loop) + "/" + str(all_loops))
        self.set_gamer2_velocity(str(velocity) + "km/h")
        if boosts == 0:
            self.set_gamer2_boost("Niedostępny")
        elif boosts == 1:
            self.set_gamer2_boost("Dostępny (1)")
        else:
            self.set_gamer2_boost("Dostępne (" + str(boosts) + ")")

    def update_info_player1(self, correct_answers, answers, curr_loop, all_loops, velocity, boosts):
        self.set_gamer1_correct_answers(str(correct_answers) + "/" + str(answers))
        self.set_gamer1_loops(str(curr_loop) + "/" + str(all_loops))
        self.set_gamer1_velocity(str(velocity) + "km/h")
        if boosts == 0:
            self.set_gamer1_boost("Niedostępny")
        elif boosts == 1:
            self.set_gamer1_boost("Dostępny (1)")
        else:
            self.set_gamer1_boost("Dostępne (" + str(boosts) + ")")

