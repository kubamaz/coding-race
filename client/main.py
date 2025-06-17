from common_fun import *
from game import game_screen
from unit_screen import unit_screen
from Loading_screen import loading_screen

MENU = 'menu'
SETTINGS = 'settings'
GAME = 'game'
SUMMARY = 'summary'

information = pygame_gui.elements.UILabel(

    relative_rect=pygame.Rect((0, -170), (1050, 80)),
    manager=manager,
    text="Zdobywasz 1 punkt do wybranego dzialu Dante!",
    anchors={'center': 'center'},
    object_id="#Information_won"
)

information2 = pygame_gui.elements.UILabel(

    relative_rect=pygame.Rect((0, -140), (800, 80)),
    manager=manager,
    text="Możesz zagrac teraz o punkt w innym dziale!",
    anchors={'center': 'center'},
    object_id="#Information_won"
)


game_title, start_button, settings_button, exit_button, volume_slider, back_button, music_volume, sound_volume, sound_slider = (
    set_elements(manager, SCREEN_HEIGHT, SCREEN_WIDTH))


current_screen = MENU
prev_screen = MENU
set_screen(current_screen, information, information2, start_button, settings_button, exit_button, volume_slider, back_button, game_title, music_volume, sound_slider, sound_volume)


while True:
    time_delta = clock.tick(60) / 1000.0

    screen.blit(background_picture, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            click_sound.play()

            if event.ui_element == start_button:
                if not networking.is_connected:
                    networking.connect()
                    networking.start_receiving()
                #NAJPIERW PRZEJDE DO EKRANU, W KTORYM BEDE WYBIERAC DZIAL W DANTE, A DOPIERO POTEM GAEM
                current_screen = GAME
                set_screen(current_screen, information, information2, start_button, settings_button, exit_button, volume_slider, back_button, game_title, music_volume, sound_slider, sound_volume)
                unit_screen()
                if loading_screen() == -1:
                    BACK_BUTTON_LOADING = False
                    current_screen = MENU
                    set_screen(current_screen, information, information2, start_button, settings_button, exit_button, volume_slider, back_button, game_title, music_volume, sound_slider, sound_volume)
                else:
                    game_screen()
                    #Po grze robie podsumowanie
                    current_screen = SUMMARY
                    prev_screen = SUMMARY
                    set_screen(current_screen, information, information2, start_button, settings_button, exit_button, volume_slider, back_button, game_title, music_volume, sound_slider, sound_volume)

                    if networking.winner == -1:
                        game_title.text = 'Server Shutdown'
                        information.text = "Serwer zostal zamkniety"
                        information.rebuild()
                        information.show()
                        information2.hide()
                    elif networking.winner == 2:
                        game_title.text = 'YOU WON - OPPONENT LEFT!'
                        information.text = "Zdobywasz 1 punkt do wybranego dzialu Dante!"
                        information.rebuild
                        information.show()
                    elif networking.winner == 1:
                        game_title.text = 'YOU WON !'
                        information.text = "Zdobywasz 1 punkt do wybranego dzialu Dante!"
                        information.rebuild
                        information.show()
                    else:
                        game_title.text = 'YOU LOST !'
                        information2.hide()
                        information.hide()

                    start_button.text = 'Play again'

                    game_title.rebuild()
                    start_button.rebuild()
            elif event.ui_element == exit_button:
                pygame.quit()
                sys.exit()
            elif event.ui_element == settings_button:
                current_screen = SETTINGS
                set_screen(current_screen, information, information2, start_button, settings_button, exit_button, volume_slider, back_button, game_title, music_volume, sound_slider, sound_volume)
                game_title.text = 'Settings'
                game_title.rebuild()
            elif event.ui_element == back_button:
                if prev_screen == MENU:
                    current_screen = MENU
                    set_screen(current_screen, information, information2, start_button, settings_button, exit_button, volume_slider, back_button, game_title, music_volume, sound_slider, sound_volume)
                    game_title.text = 'Coding Race'
                    game_title.rebuild()
                else:
                    current_screen = SUMMARY
                    set_screen(current_screen, information, information2, start_button, settings_button, exit_button, volume_slider, back_button, game_title, music_volume, sound_slider, sound_volume)
                    if networking.winner:
                        game_title.text = 'YOU WON !'
                        information.show()
                    else:
                        game_title.text = 'YOU LOST !'
                        information.hide()
                    game_title.rebuild()
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == volume_slider:
            volume = event.value
            pygame.mixer.music.set_volume(volume)
            click_sound.set_volume(volume)

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

