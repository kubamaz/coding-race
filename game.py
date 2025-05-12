from common_fun import *

background_picture = resize_img("assets/imgs/Background.png",SCREEN_HEIGHT, SCREEN_WIDTH)


exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 190, 540), (380, 80)),
        text='Exit',
        manager=manager
    )

exit_button.hide()


def game_screen():
    exit_button.show()
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        screen.blit(background_picture, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()
                if event.ui_element == exit_button:
                    exit_button.hide()
                    running = False

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


