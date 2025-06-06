from common_fun import *

BEGIN_X = -50
BEGIN_Y = 20
CAR_WIDTH = 150
CAR_HEIGHT = 100
NUMBER_OF_CARS = 8

class Car:
     def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y


red_car = Car(resize_img("assets/imgs/red-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
yellow_car = Car(resize_img("assets/imgs/yellow-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
green_car = Car(resize_img("assets/imgs/green-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
blue_car = Car(resize_img("assets/imgs/blue-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)

cars = [red_car, yellow_car, green_car, blue_car, red_car, yellow_car, green_car, blue_car]

car_number1 = 0
car_number2 = -1
round = 1

loading = True

while loading:
    screen.blit(background_picture, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loading = False


    screen.blit(cars[car_number1].img, (cars[car_number1].x, cars[car_number1].y))
    cars[car_number1].x += 2  
    if car_number2 >= 0 : 
        screen.blit(cars[car_number2].img, (cars[car_number2].x, cars[car_number2].y))
        cars[car_number2].x += 2  

    if round == 1 and cars[car_number1].x > SCREEN_WIDTH//2: #Dokladam nowy samochodzik w polowie
        car_number2+=2
        round = 2

    if cars[car_number1].x > SCREEN_WIDTH:
        cars[car_number1].x = 0
        car_number1+=2
        if car_number1 == NUMBER_OF_CARS:
            car_number1 = 0

    if cars[car_number2].x > SCREEN_WIDTH:
        cars[car_number2].x = 0
        car_number2+=2
        if car_number2 == NUMBER_OF_CARS:
            car_number2 = 0

    pygame.display.update()
    clock.tick(60)