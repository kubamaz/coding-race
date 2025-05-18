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

# TODO : uporzadkowanie kodu funkcji handle_collisions()
def handle_collisions():
    # tor
    if player1.collision_with_mask(track_border_mask, track_border_init_pos[0], track_border_init_pos[1]):
        player1.bounce_car()

    # checkpoint 1
    if player1.collision_with_mask(checkpoint1_mask, checkpoint1_init_pos[0], checkpoint1_init_pos[1]):
        if player1.answers % 3 == 0:
            player1.answers += 1
            player1.is_answering = True
            # question screen
            player1.max_velocity += 1
            right_panel.set_gamer1_correct_answers(str(player1.correct_answers) + "/" + str(player1.answers))
            player1.is_answering = False

    # checkpoint 2
    if player1.collision_with_mask(checkpoint3_mask, checkpoint3_init_pos[0], checkpoint3_init_pos[1]):
        if player1.answers % 3 == 1:
            player1.answers += 1
            player1.is_answering = True
            # question screen
            player1.max_velocity += 1
            right_panel.set_gamer1_correct_answers(str(player1.correct_answers) + "/" + str(player1.answers))
            player1.is_answering = False

    # checkpoint 3
    if player1.collision_with_mask(checkpoint2_mask, checkpoint2_init_pos[0], checkpoint2_init_pos[1]):
        if player1.answers % 3 == 2:
            player1.answers += 1
            player1.is_answering = True
            # question screen
            player1.max_velocity += 1
            right_panel.set_gamer1_correct_answers(str(player1.correct_answers) + "/" + str(player1.answers))
            player1.is_answering = False

    # finish line
    if player1.collision_with_mask(finish_mask, finish_init_pos[0], finish_init_pos[1]):
        if player1.answers in (0, 3, 6) and player1.current_loop * 3 == player1.answers:
            player1.current_loop += 1
            right_panel.set_gamer1_loops(str(player1.current_loop) + "/" + str(player1.all_loops))

        if player1.answers == 9 and player1.current_loop * 3 == player1.answers:
            player1.finished = True

def update_player2_features(finished, is_answering, velocity, max_velocity, angle, topleft_x_pos, topleft_y_pos):
    player2.finished = finished
    player2.is_answering = is_answering
    player2.velocity = velocity
    player2.max_velocity = max_velocity
    player2.angle = angle
    player2.topleft_x_pos = topleft_x_pos
    player2.topleft_y_pos = topleft_y_pos

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

# masks
finish_mask = create_mask(finish_picture)
track_border_mask = create_mask(track_border_picture)
checkpoint1_mask = create_mask(checkpoint1_picture)
checkpoint2_mask = create_mask(checkpoint2_picture)
checkpoint3_mask = create_mask(checkpoint3_picture)

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
# TODO : uzależnienie pozycji start_topleft_y od kolejności połączenia z serwerem -
#  - jeden z graczy na poczatku musi byc wyżej, a drugi niżej


def game_screen():
    # exit_button.show()
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        prepare_screen(screen)

        # player 1
        player1.handle_pressed_keys()

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

        # player 2

        # TODO : AKTUALIZACJA POZYCJI
        # update_player2_position(...)
        player2.blit_car()

        # TODO : AKTUALIZACJA INFORMACJI NA PANELU WYNIKOW
        # right_panel.update_info_player2(...)

        # kolizje
        handle_collisions()

        # prawy panel
        right_panel.set_gamer1_velocity(player1.get_real_velocity_str() + "km/h")
        right_panel.blit_panel()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


game_screen()
