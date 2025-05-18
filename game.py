from common_fun import *
from ScorePanel import *
from Player import *


def prepare_screen(my_screen):
    my_screen.blit(background_picture, background_init_pos)
    my_screen.blit(track_picture, track_init_pos)
    my_screen.blit(finish_picture, finish_init_pos)
    my_screen.blit(track_border_picture, track_border_init_pos)
    my_screen.blit(checkpoint1_picture, checkpoint1_init_pos)
    my_screen.blit(checkpoint2_picture, checkpoint2_init_pos)
    my_screen.blit(checkpoint3_picture, checkpoint3_init_pos)


# images
background_picture = resize_img("assets/imgs/Background.png", SCREEN_HEIGHT, SCREEN_WIDTH)
track_picture = resize_img("assets/imgs/track.png", SCREEN_HEIGHT, SCREEN_WIDTH)
track_border_picture = resize_img("assets/imgs/track_border.png", SCREEN_HEIGHT, SCREEN_WIDTH)
finish_picture = pygame.transform.rotate(pygame.image.load("assets/imgs/finish.png"), 90)
checkpoint1_picture = resize_img("assets/imgs/checkpoints.png", 70, 120)
checkpoint2_picture = resize_img("assets/imgs/checkpoints.png", 70, 120)
checkpoint3_picture = resize_img("assets/imgs/checkpoints.png", 70, 120)
checkpoint3_picture = pygame.transform.flip(checkpoint3_picture, flip_x=False, flip_y=True)
checkpoint3_picture = pygame.transform.rotate(checkpoint3_picture, 45)

# init positions
background_init_pos = (0, 0)
track_init_pos = (0, 0)
finish_init_pos = (600, 15)
track_border_init_pos = (0, 0)
checkpoint1_init_pos = (180, 230)
checkpoint2_init_pos = (910, 500)
checkpoint3_init_pos = (300, 665)

# panel
right_panel = ScorePanel(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
right_panel.add_components()


exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 190, 540), (380, 80)),
        text='Exit',
        manager=manager
    )

exit_button.hide()

# players
player1 = Player(screen, "assets/imgs/red-car.png", 625, 35)
player2 = Player(screen, "assets/imgs/purple-car.png", 625, 75)


def game_screen():
    # exit_button.show()
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        prepare_screen(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()
                if event.ui_element == exit_button:
                    # exit_button.hide()
                    running = False

            manager.process_events(event)

        # players
        player1.blit_car()
        player2.blit_car()

        # prawy panel
        right_panel.blit_panel()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


game_screen()
