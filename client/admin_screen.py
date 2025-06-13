import pygame
import pygame_gui

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Panel administratora")
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))


class AdminPanel:
    def __init__(self, screen, manager, back_callback):
        self.screen = screen
        self.manager = manager
        self.back_callback = back_callback

        # Panel główny
        self.main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            manager=manager
        )

        # Przyciski w panelu głównym
        self.btn_questions = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, 50, 200, 50),
            text="Zarządzaj pytaniami",
            manager=manager,
            container=self.main_panel
        )

        self.btn_users = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, 120, 200, 50),
            text="Zarządzaj użytkownikami",
            manager=manager,
            container=self.main_panel
        )

        self.btn_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, 500, 100, 40),
            text="Powrót",
            manager=manager,
            container=self.main_panel
        )

    def handle_events(self, event):
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_questions:
                print("Kliknięto: Zarządzaj pytaniami")
            elif event.ui_element == self.btn_users:
                print("Kliknięto: Zarządzaj użytkownikami")
            elif event.ui_element == self.btn_back:
                print("Kliknięto: Powrót")
                self.back_callback()


def back_to_main_menu():
    print("Powrót do menu głównego")


admin_panel = AdminPanel(screen, manager, back_to_main_menu)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        admin_panel.handle_events(event)
        manager.process_events(event)

    manager.update(time_delta)

    screen.fill((0, 0, 0))
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
