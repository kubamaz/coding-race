import pygame
import pygame_gui
import subprocess
import sys
import json
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832
window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ekran startowy')


background_color = (255,153,68)


manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

input_width = 300
input_height = 40
input_x = (SCREEN_WIDTH - input_width) // 2

login_y = 250
password_y = 320
button_y = 400

login_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((input_x, login_y), (input_width, input_height)),
    manager=manager
)

password_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((input_x, password_y), (input_width, input_height)),
    manager=manager
)

password_input.set_text_hidden(True) 

login_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((input_x - 100, login_y), (100, input_height)),
    text='Login:',
    manager=manager
)

password_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((input_x - 100, password_y), (100, input_height)),
    text='Hasło:',
    manager=manager
)

login_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((input_x, button_y), (input_width, 40)),
    text='Zaloguj',
    manager=manager
)
error_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((input_x, button_y + 60), (input_width, 40)),
    text='',
    manager=manager,
)
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == login_button:
                    login_text = login_input.get_text()
                    password_text = password_input.get_text()

                    try:
                        with open('users.json', 'r') as f:
                            data = json.load(f)
                        
                        found_user = None
                        for user in data['users']:
                            if(user['login'] == login_text and user['password'] == password_text):
                                found_user = user
                                break
                        if found_user:
                            if found_user['role'] == 'student':
                                pygame.quit()
                                subprocess.run([sys.executable, 'main.py'])
                            elif found_user['role'] == 'admin':
                                #do uzupełnienia po zrobieniu panelu administratora
                                print("zalogowano jako administrator")
                        else:
                            error_label.set_text('❌ Nieprawidłowy login lub hasło.')
                    except FileNotFoundError:
                        error_label.set_text('❌ Brak pliku users.json.')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill(background_color)
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
