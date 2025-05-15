import pygame
import pygame_gui
import sys


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832
POINTS = 0
answered_questions = []

# To bedziemy mogli umiescic pozniej w jakiejs bazie danych uzytkownika zeby odpowiednie dzialy byly zablokowane
UNITS = ['1. Pliki', '2. Struktury', '3. Unie', '4. Dynamiczna alokacja pamięci I',
         '5. Dynamiczna alokacja pamięci II', '6. Dynamiczna alokacja pamięci - teksty i napisy',
         '7. Wskaźniki do funkcji', '8. Funkcje ze zmienną liczbą argumentów i argumenty funkcji main',
         '9. Operacje bitowe oraz dyrektywy preprocesora', '10. Dynamiczne struktury danych']


result = 1 #To jest stala ktora okresla czy wygralismy czy przegralismy: 0 - przegrana, 1 - wygrana

#Ustawia dźwięk muzyki w tle ekranu głównego i zwraca dźwięk klikania
def set_sounds(music_volume, click_volume):
    # Ekran główny muzyka
    pygame.mixer.music.load("assets/Sounds/background.mp3")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)

    # Dźwięk klikania
    click_sound = pygame.mixer.Sound("assets/Sounds/click.wav")
    click_sound.set_volume(click_volume)

    return click_sound



def resize_img(img, height, width):
    pic = pygame.image.load(img)
    return pygame.transform.scale(pic, (width, height))

def set_elements(manager, screen_height, screen_width):

    game_title = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0, -240), (600, 90)),
        text='Coding Race',
        manager=manager,
        object_id='#game_title',
        anchors={'center': 'center'}
    )

    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((screen_width // 2 - 190, 300), (380, 80)),
        text='Start',
        manager=manager
    )
    settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((screen_width // 2 - 190, 420), (380, 80)),
        text='Settings',
        manager=manager
    )
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((screen_width // 2 - 190, 540), (380, 80)),
        text='Exit',
        manager=manager
    )

    volume_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((490, 350), (300, 50)),
        start_value=0.5,
        value_range=(0.0, 1.0),
        manager=manager
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((screen_width // 2 - 190, 450), (380, 80)),
        text='Back',
        manager=manager
    )
    volume_slider.hide()
    back_button.hide()
    return game_title, start_button, settings_button, exit_button, volume_slider, back_button

def set_screen(current_screen, Information, Information2, start_button, settings_button, exit_button, volume_slider, back_button, game_title):
    if current_screen == 'menu':
        Information.hide()
        Information2.hide()
        start_button.show()
        settings_button.show()
        exit_button.show()
        volume_slider.hide()
        back_button.hide()
    elif current_screen == 'settings':
        Information.hide()
        Information2.hide()
        start_button.hide()
        settings_button.hide()
        exit_button.hide()
        volume_slider.show()
        back_button.show()
    elif current_screen == 'game':
        Information.hide()
        Information2.hide()
        game_title.hide()
        start_button.hide()
        settings_button.hide()
        exit_button.hide()
        volume_slider.hide()
        back_button.hide()
    elif current_screen == 'summary':
        Information.show()
        Information2.show()
        game_title.show()
        start_button.show()
        settings_button.show()
        exit_button.show()
        volume_slider.hide()
        back_button.hide()

#Ustawienia dla wszystkich ekranow

pygame.init()
pygame.mixer.init()
click_sound = set_sounds(0.5, 0.6) #Ustawiam click_sound do wszystkich ekranow

# Ustawianie ekranu głównego
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("CODING RACE")

#Ustawianie tla
background_picture = resize_img("assets/imgs/Background_pic.png",SCREEN_HEIGHT, SCREEN_WIDTH)

#Ustawianie elementow na ekranie głównym
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")

clock = pygame.time.Clock()
