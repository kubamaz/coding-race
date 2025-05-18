from ScorePanel import *


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

    # blit
    def blit_car(self):
        rotated_image = pygame.transform.rotate(self.car_when_driving, self.angle)
        if self.is_answering:
            rotated_image.set_alpha(128)
        self.screen.blit(rotated_image, (self.topleft_x_pos, self.topleft_y_pos))

