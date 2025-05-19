from ScorePanel import *
from math import radians, sin, cos

class Player:
    def __init__(self, my_screen, car_when_driving, start_topleft_x, start_topleft_y):
        # screen init
        self.screen = my_screen

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

        # car position
        self.topleft_x_pos = start_topleft_x
        self.topleft_y_pos = start_topleft_y

        # others
        self.epsilon = 0.25

    # blit
    def blit_car(self):
        rotated_image = pygame.transform.rotate(self.car_when_driving, self.angle)
        if self.is_answering:
            rotated_image.set_alpha(128)
        self.screen.blit(rotated_image, (self.topleft_x_pos, self.topleft_y_pos))

    # moving logic
    def move_forward(self):
        if self.velocity >= 0:
            self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
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
        if to_left:
            self.angle += self.rotation
        if to_right:
            self.angle -= self.rotation

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

            if keys[pygame.K_w]:
                position_change = True
                self.move_forward()
            if keys[pygame.K_s]:
                position_change = True
                self.move_backward()
            if keys[pygame.K_a]:
                self.rotate_car(to_left=True)
            if keys[pygame.K_d]:
                self.rotate_car(to_right=True)

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

