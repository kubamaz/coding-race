from common_fun import *

BEGIN_X = -30
BEGIN_Y = 100
CAR_WIDTH = 150
CAR_HEIGHT = 100
NUMBER_OF_CARS = 4

class Car:
     def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y


red_car = Car(resize_img("assets/imgs/red-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
yellow_car = Car(resize_img("assets/imgs/yellow-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
green_car = Car(resize_img("assets/imgs/green-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
blue_car = Car(resize_img("assets/imgs/blue-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)

cars = [red_car, yellow_car, green_car, blue_car]

car_number = 0
loading = True

while loading:
    screen.blit(background_picture, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loading = False


    screen.blit(cars[car_number].img, (cars[car_number].x, cars[car_number].y))
    cars[car_number].x += 2  

    if cars[car_number].x > SCREEN_WIDTH:
        cars[car_number].x = 0
        car_number+=1
        if car_number == NUMBER_OF_CARS:
            car_number = 0

    pygame.display.update()
    clock.tick(60)