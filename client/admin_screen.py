import pygame
import pygame_gui

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832

def main():
    pygame.init()
    pygame.display.set_caption("Panel administratora")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    main_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
        manager=manager
    )

    btn_questions = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(50, 50, 200, 50),
        text="Zarządzaj pytaniami",
        manager=manager,
        container=main_panel
    )

    btn_users = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(50, 120, 200, 50),
        text="Zarządzaj użytkownikami",
        manager=manager,
        container=main_panel
    )

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btn_questions:
                    print("Kliknięto: Zarządzaj pytaniami")
                elif event.ui_element == btn_users:
                    print("Kliknięto: Zarządzaj użytkownikami")

            manager.process_events(event)

        manager.update(time_delta)
        screen.fill((0, 0, 0))
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
