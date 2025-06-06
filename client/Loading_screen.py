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

cars = [red_car, yellow_car, green_car, blue_car]

car_number1 = 0
car_number2 = -1
car_number3 = -1
car_number4 = -1

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
    if car_number3 >= 0 : 
        screen.blit(cars[car_number3].img, (cars[car_number3].x, cars[car_number3].y))
        cars[car_number3].x += 2  
    if car_number4 >= 0 : 
        screen.blit(cars[car_number4].img, (cars[car_number4].x, cars[car_number4].y))
        cars[car_number4].x += 2  

    if car_number2 == -1 and cars[car_number1].x > SCREEN_WIDTH//4: #Dokladam nowy samochodzik w polowie
        car_number2+=2

    if car_number3 == -1 and cars[car_number1].x > SCREEN_WIDTH//2: #Dokladam nowy samochodzik w polowie
        car_number3+=3

    if car_number4 == -1 and cars[car_number1].x > (SCREEN_WIDTH//2 + SCREEN_WIDTH//4): #Dokladam nowy samochodzik w polowie
        car_number4+=4

    if cars[car_number1].x > SCREEN_WIDTH:
        cars[car_number1].x = BEGIN_X

    if car_number2 != -1 and cars[car_number2].x > SCREEN_WIDTH:
        cars[car_number2].x = BEGIN_X

    
    if car_number3!= -1 and cars[car_number3].x > SCREEN_WIDTH:
        cars[car_number3].x = BEGIN_X

    if car_number4!= -1 and cars[car_number4].x > SCREEN_WIDTH:
        cars[car_number4].x = BEGIN_X

    pygame.display.update()
    clock.tick(60)