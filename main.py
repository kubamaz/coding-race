from game import *

MENU = 'menu'
SETTINGS = 'settings'
GAME = 'game'

pygame.init()
pygame.mixer.init()

click_sound = set_sounds(0.5, 0.6)

# Ustawianie ekranu głównego
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("CODING RACE")

#Ustawianie tla
background_picture = resize_img("assets/imgs/Background_pic.png",SCREEN_HEIGHT, SCREEN_WIDTH)

#Ustawianie elementow na ekranie głównym
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")
game_title, start_button, settings_button, exit_button, volume_slider, back_button = (
    set_elements(manager, SCREEN_HEIGHT, SCREEN_WIDTH))


clock = pygame.time.Clock()


while True:
    time_delta = clock.tick(60) / 1000.0

    screen.blit(background_picture, (0, 0))
    current_screen = MENU

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            click_sound.play()

            if event.ui_element == start_button:
                #NAJPIERW PRZEJDE DO EKRANU, W KTORYM BEDE WYBIERAC DZIAL W DANTE, A DOPIERO POTEM GAEM
                current_screen = GAME
                set_screen(current_screen, start_button, settings_button, exit_button, volume_slider, back_button)
                game_screen()
            elif event.ui_element == exit_button:
                pygame.quit()
                sys.exit()
            elif event.ui_element == settings_button:
                current_screen = SETTINGS
                set_screen(current_screen, start_button, settings_button, exit_button, volume_slider, back_button)
            elif event.ui_element == back_button:
                current_screen = MENU
                set_screen(current_screen, start_button, settings_button, exit_button, volume_slider, back_button)

        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == volume_slider:
            volume = event.value
            pygame.mixer.music.set_volume(volume)
            click_sound.set_volume(volume)

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

