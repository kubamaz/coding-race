import pygame
import pygame_gui
import subprocess
import sys
import json
import math
from admin_screen import run_admin_panel
pygame.init()




SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832
window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ekran startowy')
background_image = pygame.image.load("assets/imgs/background.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def create_circular_masked_surface(surface, feather_radius):
    width, height = surface.get_size()
    center_x = width // 2
    center_y = height // 2
    max_radius = min(center_x, center_y)

    masked_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < (max_radius - feather_radius):
                alpha = 255
            elif dist < max_radius:
                fade = (max_radius - dist) / feather_radius
                alpha = int(255 * (fade ** 2)) 
            else:
                alpha = 0

            r, g, b, a = surface.get_at((x, y))
            masked_surface.set_at((x, y), (r, g, b, min(alpha, a)))

    return masked_surface

original_logo = pygame.image.load("assets/imgs/logo.png").convert_alpha()
scale_factor = 0.3
logo_size = (int(original_logo.get_width() * scale_factor), int(original_logo.get_height() * scale_factor))
scaled_logo = pygame.transform.smoothscale(original_logo, logo_size)
logo = create_circular_masked_surface(scaled_logo, feather_radius=10)

background_color = (255, 217, 179)


manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")

input_width = 300
input_height = 40
input_x = (SCREEN_WIDTH - input_width) // 2

login_y = 250
password_y = 320
button_y = 400

login_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((input_x, login_y), (input_width, input_height)),
    manager=manager,
    object_id="#login_input"
)

password_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((input_x, password_y), (input_width, input_height)),
    manager=manager,
    object_id="#password_input"
)

password_input.set_text_hidden(True) 

login_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((input_x - 100, login_y), (100, input_height)),
    text='Login:',
    manager=manager,
    object_id="#login_label"
)

password_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((input_x - 100, password_y), (100, input_height)),
    text='Hasło:',
    manager=manager,
    object_id="#password_label"
)

login_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((input_x, button_y), (input_width, 40)),
    text='Zaloguj',
    manager=manager,
    object_id='#login_button'
)
error_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((input_x, button_y + 60), (input_width, 40)),
    text='',
    manager=manager,
    object_id="#error_label"
)
clock = pygame.time.Clock()
is_running = True
next_action = None
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
                                next_action = "student"
                                is_running = False
                                pygame.quit()
                                print("Uruchamiam main.py jako student...")
                                subprocess.run([sys.executable, 'main.py'])
                            elif found_user['role'] == 'admin':
                                is_running = False
                                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                                run_admin_panel()
                        else:
                            error_label.set_text('Nieprawidłowy login lub hasło.')
                    except FileNotFoundError:
                        error_label.set_text('Brak pliku users.json.')
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if login_input.is_focused:
                    login_input.unfocus()
                    password_input.focus()
                elif password_input.is_focused:
                    password_input.unfocus()
                    login_input.focus()
                else:
                    login_input.focus()

            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Udaj kliknięcie przycisku "Zaloguj"
                fake_event = pygame.event.Event(pygame.USEREVENT, {
                    'user_type': pygame_gui.UI_BUTTON_PRESSED,
                    'ui_element': login_button
                })
                pygame.event.post(fake_event)


        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background_image, (0,0))
    
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fog_surface.set_alpha(80)
    fog_surface.fill((200, 200, 200))
    window_surface.blit(fog_surface, (0, 0))

    manager.draw_ui(window_surface)
        # Oblicz pozycję do wyśrodkowania logo
    logo_x = (SCREEN_WIDTH - logo.get_width()) // 2
    logo_y = login_y - logo.get_height() - 40  # odstęp nad loginem

    # Rysuj logo
    window_surface.blit(logo, (logo_x, logo_y))
    pygame.display.update()

pygame.quit()
