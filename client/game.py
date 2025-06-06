from Player import *
from Question_screen import *
import common_fun

def prepare_screen(my_screen):
    my_screen.blit(background_picture, background_init_pos)
    my_screen.blit(track_picture, track_init_pos)
    my_screen.blit(finish_picture, finish_init_pos)
    my_screen.blit(track_border_picture, track_border_init_pos)
    my_screen.blit(checkpoint1_picture, checkpoint1_init_pos)
    my_screen.blit(checkpoint2_picture, checkpoint2_init_pos)
    my_screen.blit(checkpoint3_picture, checkpoint3_init_pos)


def handle_correct_answer():
    player1.max_velocity += 1
    player1.correct_answers += 1
    player1.correct_answers_in_a_row += 1
    if player1.correct_answers_in_a_row == 3:
        player1.boosts += 1
        player1.correct_answers_in_a_row = 0
        update_player1_boosts()


def handle_incorrect_answer():
    player1.correct_answers_in_a_row = 0


def handle_checkpoints_collisions():
    for checkpoint_id in range(1, len(checkpoint_masks) + 1):
        if player1.collision_with_mask(checkpoint_masks[checkpoint_id - 1], checkpoint_init_poses[checkpoint_id - 1][0],
                                       checkpoint_init_poses[checkpoint_id - 1][1]):
            if player1.answers % 3 == int(checkpoint_id - 1):
                player1.answers += 1
                player1.is_answering = True
                # question screen
                if question_screen():
                    handle_correct_answer()
                else:
                    handle_incorrect_answer()
                right_panel.set_gamer1_correct_answers(str(player1.correct_answers) + "/" + str(player1.answers))
                player1.is_answering = False


def handle_track_border_collisions():
    if player1.collision_with_mask(track_border_mask, track_border_init_pos[0], track_border_init_pos[1]):
        player1.bounce_car()


def handle_finish_line_collisions():
    if player1.collision_with_mask(finish_mask, finish_init_pos[0], finish_init_pos[1]):
        if player1.answers in (0, 3, 6) and player1.current_loop * 3 == player1.answers:
            player1.current_loop += 1
            right_panel.set_gamer1_loops(str(player1.current_loop) + "/" + str(player1.all_loops))

        if player1.answers == 9 and player1.current_loop * 3 == player1.answers:
            player1.finished = True

def handle_players_collision():
    if player1.is_answering == False and player2.is_answering == False:
        if player1.collision_with_player(player2):
            player1.bounce_car()
            player2.bounce_car()



def handle_collisions():
    # tor
    handle_track_border_collisions()

    # checkpointy
    handle_checkpoints_collisions()

    # finish line
    handle_finish_line_collisions()

    # kolizja z drugim autem
    handle_players_collision()


def update_player1_boosts():
    if player1.boosts == 0:
        right_panel.set_gamer1_boost("Niedostępny")
    elif player1.boosts == 1:
        right_panel.set_gamer1_boost("Dostępny (1)")
    else:
        right_panel.set_gamer1_boost("Dostępne (" + str(player1.boosts) + ")")


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

checkpoint_masks = (checkpoint1_mask, checkpoint3_mask, checkpoint2_mask)

# init positions
background_init_pos = (0, 0)
track_init_pos = (0, 0)
finish_init_pos = (600, 15)
track_border_init_pos = (0, 0)
checkpoint1_init_pos = (180, 230)
checkpoint2_init_pos = (910, 500)
checkpoint3_init_pos = (300, 665)

checkpoint_init_poses = (checkpoint1_init_pos, checkpoint3_init_pos, checkpoint2_init_pos)

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
player1 = Player(screen, "assets/imgs/red-car.png", 625, 35, track_border_mask, track_border_init_pos)
player2 = Player(screen, "assets/imgs/purple-car.png", 625, 75, track_border_mask, track_border_init_pos)
# TODO : uzależnienie pozycji start_topleft_y od kolejności połączenia z serwerem -
#  - jeden z graczy na poczatku musi byc wyżej, a drugi niżej



# Rysowanie w pętli gry, PRZED pygame.display.update()

counter = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((-20, -50), (500, 500)),
        text = '3',
        manager=manager,
        object_id='#counting',
        anchors={'center': 'center'}
)
counter.hide()

def game_screen():
    start_time = pygame.time.get_ticks()
    time_counter = 3

    player1.reset_everything()
    player2.reset_everything()
    right_panel.update_info_player2(player2.correct_answers, player2.correct_answers, player2.current_loop, player2.all_loops, player2.velocity, player2.boosts)
    right_panel.update_info_player1(player2.correct_answers, player2.correct_answers, player2.current_loop, player2.all_loops, player2.velocity, player2.boosts)

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # RGBA: czarny z przezroczystością
    counter.text = str(time_counter)
    # exit_button.show()
    running = True
    counter.show()
    while running:
        time_delta = clock.tick(60) / 1000.0
        current_time = pygame.time.get_ticks()

        #USTAWIAM PRZEZROCZYSTE TLO DLA PIERWSZYCH 3 SEKUND
        if time_counter > 0:
            if current_time - start_time >= 1000:
                start_time = current_time
                time_counter -= 1
                counter.text = str(time_counter)
                counter.rebuild()
                if time_counter == 0:
                    counter.hide()

            # Rysuj grę normalnie
            prepare_screen(screen)
            # Przezroczysta nakładka na ekran
            screen.blit(overlay, (0, 0))

            manager.update(time_delta)
            manager.draw_ui(screen)
            pygame.display.flip()
            continue 

        counter.hide()
        prepare_screen(screen)
        


        # player 1
        player1.handle_pressed_keys()
        update_player1_boosts()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            #     click_sound.play()
            #     if event.ui_element == exit_button:
            #         exit_button.hide()
            #         common_fun.RESULT = 1
            #         running = False

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

        # czy koniec gry
        if player1.finished:
            common_fun.RESULT = 1
            break
        elif player2.finished:
            common_fun.RESULT = 0
            break

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


game_screen()
