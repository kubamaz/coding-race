import sys

from home_screen import *

pygame.init()

# Ustawienia ekranu
click_sound = set_sounds(0.5, 0.6)
background_picture = resize_img("assets/imgs/Background_pic.png",SCREEN_HEIGHT, SCREEN_WIDTH)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CODING RACE")

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")



game_title = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0, -220), (600, 90)),
        text='CHOOSE UNIT',
        manager=manager,
        object_id='#Unit_selection',
        anchors={'center': 'center'}
    )

dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=UNITS,
    starting_option=UNITS[0],
    relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 500, 300), (1030, 60)),
    manager=manager,
)

OK_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, 450), (200, 80)),
        text="OK",
        manager=manager
    )


clock = pygame.time.Clock()


def unit_screen():
    running = True
    selected_unit = UNITS[0]
    while running:
        time_delta = clock.tick(60) / 1000.0

        screen.blit(background_picture, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Obsługa wyboru opcji z listy
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                click_sound.play()
                selected_unit = event.text
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()
                if event.ui_element == OK_button:
                    running = False
            manager.process_events(event)


        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    return selected_unit
