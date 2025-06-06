from common_fun import *
from unit_screen import unit_screen

BEGIN_X = -50
BEGIN_Y = 20
CAR_WIDTH = 150
CAR_HEIGHT = 100
NUMBER_OF_CARS = 8


waiting_information = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0,-200), (1500, 400)),
        text='POSZUKIWANIE UCZESTNIKA',
        manager=manager,
        object_id="#game_title",
        anchors={'center': 'center'}
)
please_wait = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0,-100), (1500, 400)),
        text='PROSZE CZEKAC',
        manager=manager,
        anchors={'center': 'center'}
)

back_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20), (380, 80)),
    text='Back',
    manager=manager
)

#Obsluga samochodzikow
class Car:
     def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y


def cars_conf():
    red_car = Car(resize_img("assets/imgs/red-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
    yellow_car = Car(resize_img("assets/imgs/yellow-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
    green_car = Car(resize_img("assets/imgs/green-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
    blue_car = Car(resize_img("assets/imgs/blue-car-side.png", CAR_HEIGHT, CAR_WIDTH), BEGIN_X, BEGIN_Y)
    cars = [red_car, yellow_car, green_car, blue_car]

    return cars


waiting_information.hide()
please_wait.hide()
back_button.hide()
def loading_screen():
    logowanie_uzytkownika = 5 #SYMULACJA ZE PO 5 SEKUNDACH UZYTKOWNIK SIE ZALOGUJE - USUNAC TO POZNIEJ!!!!!!!!
    loading = True
    start_time = pygame.time.get_ticks()
    waiting_information.show()
    please_wait.show()
    back_button.show()
    number_of_dots = 1

    cars = cars_conf()
    car_number1 = 0
    car_number2 = -1
    car_number3 = -1
    car_number4 = -1

    while loading:
        current_time = pygame.time.get_ticks()
        time_delta = clock.tick(60) / 1000.0
        screen.blit(background_picture, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loading = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()
                if event.ui_element == back_button:
                    waiting_information.hide()
                    please_wait.hide()
                    back_button.hide()
                    unit_screen()
            manager.process_events(event)




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

        if current_time - start_time >= 1000:
            start_time = current_time
            please_wait.text = 'PROSZE CZEKAC' + number_of_dots*'.'
            number_of_dots += 1
            if number_of_dots == 4:
                number_of_dots = 0
            please_wait.rebuild()

            #CO SEKUNDE BEDE TEZ SPRAWDZAC CZY JAKIS UZYTKOWNIK SIE NIE ZALOGOWAL - TERAZ PRZYJMUJE ZE PO 5 SEKUNDACH SIE ZALOGUJE
            logowanie_uzytkownika -= 1
            if logowanie_uzytkownika == 0:
                waiting_information.hide()
                please_wait.hide()
                back_button.hide()
                loading = False


        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()
