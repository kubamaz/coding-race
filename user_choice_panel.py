import pygame
import pygame_gui
import subprocess
import sys
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832
window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ekran startowy')


background_color = (255,153,68)


manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
button_width = 200
button_height = 50
button_x = (SCREEN_WIDTH - button_width) // 2

admin_y = 200
student_y = 300
# Przycisk "Admin"
admin_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((button_x, admin_y), (button_width, button_height)),
    text='Admin',
    manager=manager
)

# Przycisk "Student"
student_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((button_x, student_y), (button_width, button_height)),
    text='Student',
    manager=manager
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
                if event.ui_element == admin_button:
                    
                    print("Przejście do panelu administratora")
                if event.ui_element == student_button:
                    is_running = False
                    pygame.quit()
                    subprocess.run([sys.executable, 'main.py'])
                    print("Przejście do panelu studenta")

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill(background_color)
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
