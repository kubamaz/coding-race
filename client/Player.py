import pygame

from ScorePanel import *
from math import radians, sin, cos


class Player:
    def __init__(self, my_screen, car_when_driving, start_topleft_x, start_topleft_y, track_border_mask,
                 track_border_init_pos):
        # screen init
        self.screen = my_screen

        # track border mask
        self.track_border_mask = track_border_mask
        self.track_border_init_pos = track_border_init_pos

        # booleans
        self.finished = False
        self.is_answering = False

        # loops information
        self.current_loop = 0
        self.all_loops = 3

        # answers information
        self.answers = 0
        self.correct_answers = 0
        self.correct_answers_in_a_row = 0

        # boosts information
        self.boosts = 0
        self.boost_max_velocity = 15

        self.is_boosting = False
        self.boost_start_time = 0
        self.boost_duration = 1000

        # car features
        self.velocity = 0
        self.velocity_factor = 10
        self.max_velocity = 4
        self.angle = 90
        self.acceleration = 5
        self.rotation = 6

        # car image
        scale_car = 0.6
        self.car_when_driving = resize_img(car_when_driving, 76 * scale_car, 38 * scale_car)
        self.rotated_image = self.car_when_driving

        # car position
        self.topleft_x_pos = start_topleft_x
        self.topleft_y_pos = start_topleft_y

        # car start position
        self.start_topleft_x = start_topleft_x
        self.start_topleft_y = start_topleft_y


        # others
        self.epsilon = 0.25

    # blit
    def blit_car(self):
        self.rotated_image = pygame.transform.rotate(self.car_when_driving, self.angle)
        self.update_boost()
        rotated_image = pygame.transform.rotate(self.car_when_driving, self.angle)
        if self.is_answering:
            rotated_image.set_alpha(128)
        self.screen.blit(rotated_image, (self.topleft_x_pos, self.topleft_y_pos))

    # moving logic
    def move_forward(self):
        if self.velocity >= 0:
            max_speed = self.boost_max_velocity if self.is_boosting else self.max_velocity
            self.velocity = min(self.velocity + self.acceleration, max_speed)
            self.move_car()
        else:
            self.reduce_speed()

    def move_backward(self):
        if self.velocity <= 0:
            self.velocity = max(self.velocity - self.acceleration, -self.max_velocity)
            self.move_car()
        else:
            self.reduce_speed()

    def rotate_car(self, to_left=False, to_right=False):
        prev_angle = self.angle
        if to_left:
            self.angle += self.rotation
        if to_right:
            self.angle -= self.rotation

        if self.collision_with_mask(self.track_border_mask,
                                    self.track_border_init_pos[0], self.track_border_init_pos[1]):
            self.angle = prev_angle

    def reduce_speed(self):
        if self.velocity >= 0:
            self.velocity = self.velocity - self.acceleration / 4
            if self.velocity < 0:
                self.velocity = 0
        else:
            self.velocity = self.velocity + self.acceleration / 4
            if self.velocity > 0:
                self.velocity = 0

        if abs(self.velocity) <= self.epsilon:
            self.velocity = 0
        self.move_car()

    def bounce_car(self):
        self.velocity = -self.velocity
        self.move_car()

    def move_car(self):
        rads = radians(self.angle)
        self.topleft_y_pos -= self.velocity * cos(rads)
        self.topleft_x_pos -= self.velocity * sin(rads)

    # handle events
    def handle_pressed_keys(self):
        if not self.finished:
            position_change = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                position_change = True
                self.move_forward()
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                position_change = True
                self.move_backward()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rotate_car(to_left=True)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rotate_car(to_right=True)
            if keys[pygame.K_SPACE]:
                position_change = True
                self.use_boost()

            if not position_change:
                self.reduce_speed()

        self.blit_car()

    # collisions
    def collision_with_mask(self, mask, mask_x, mask_y):
        rotated_image = pygame.transform.rotate(self.car_when_driving, self.angle)
        car_mask = pygame.mask.from_surface(rotated_image)
        offset = (int(self.topleft_x_pos - mask_x), int(self.topleft_y_pos - mask_y))
        return mask.overlap(car_mask, offset) is not None

    def get_car_rect(self):
        return self.car_when_driving.get_rect(topleft=(self.topleft_x_pos, self.topleft_y_pos))

    # to score panel
    def get_real_velocity_str(self):
        real_velocity = self.velocity * self.velocity_factor
        return str(abs(real_velocity))

    def use_boost(self):
        if self.boosts > 0 and not self.is_boosting:
            self.is_boosting = True
            self.boost_start_time = pygame.time.get_ticks()
            self.boosts -= 1

    def update_boost(self):
        if self.is_boosting:
            current_time = pygame.time.get_ticks()
            if current_time - self.boost_start_time >= self.boost_duration:
                self.is_boosting = False

    def reset_everything(self):
        # booleans
        self.finished = False
        self.is_answering = False

        # loops information
        self.current_loop = 0
        self.all_loops = 3

        # answers information
        self.answers = 0
        self.correct_answers = 0
        self.correct_answers_in_a_row = 0

        # boosts information
        self.boosts = 0
        self.boost_max_velocity = 15

        self.is_boosting = False
        self.boost_start_time = 0
        self.boost_duration = 1000

        # car features
        self.velocity = 0
        self.velocity_factor = 10
        self.max_velocity = 4
        self.angle = 90
        self.acceleration = 5
        self.rotation = 6


        # car position
        self.topleft_x_pos = self.start_topleft_x
        self.topleft_y_pos = self.start_topleft_y

    def collision_with_player(self, other_player):
        self_mask = pygame.mask.from_surface(self.rotated_image)
        other_mask = pygame.mask.from_surface(other_player.rotated_image)

        offset_x = other_player.topleft_x_pos - self.topleft_x_pos
        offset_y = other_player.topleft_y_pos - self.topleft_y_pos

        overlap = self_mask.overlap(other_mask, (offset_x, offset_y))
        return overlap is not None

