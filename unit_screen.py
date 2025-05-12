from common_fun import *


game_title = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0, -220), (600, 90)),
        text='CHOOSE UNIT',
        manager=manager,
        object_id='#game_title',
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

game_title.hide()
dropdown.hide()
OK_button.hide()


def unit_screen():
    game_title.show()
    dropdown.show()
    OK_button.show()
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
                selected_unit = event.text
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()
                if event.ui_element == OK_button:
                    running = False
                    game_title.hide()
                    dropdown.hide()
                    OK_button.hide()
            manager.process_events(event)


        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    return selected_unit
