import pygame
import pygame_gui

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832

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

        relative_rect=pygame.Rect((0, -220), (470, 80)),
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

def set_screen(current_screen, start_button, settings_button, exit_button, volume_slider, back_button):
    if current_screen == 'menu':
        start_button.show()
        settings_button.show()
        exit_button.show()
        volume_slider.hide()
        back_button.hide()
    elif current_screen == 'settings':
        start_button.hide()
        settings_button.hide()
        exit_button.hide()
        volume_slider.show()
        back_button.show()
    elif current_screen == 'game':
        start_button.hide()
        settings_button.hide()
        exit_button.hide()
        volume_slider.hide()
        back_button.hide()
