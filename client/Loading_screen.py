from common_fun import *

BEGIN_X = 0
BEGIN_Y = 100
CAR_WIDTH = 150
CAR_HEIGHT = 100

class Car:
     def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y


red_car = Car(resize_img("assets/imgs/red-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
yellow_car = Car(resize_img("assets/imgs/yellow-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
green_car = Car(resize_img("assets/imgs/green-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
blue_car = Car(resize_img("assets/imgs/blue-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)




loading = True
while loading:
    screen.blit(background_picture, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loading = False


    # Rysuj samochód
    screen.blit(red_car.img, (red_car.x, red_car.y))
    red_car.x += 2  # Samochód jedzie w prawo

    # Przerwij "ładowanie" po pewnym czasie
    if red_car.x > SCREEN_WIDTH:
        loading = False

    pygame.display.update()
    clock.tick(60)