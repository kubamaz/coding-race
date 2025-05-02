import pygame
import pygame_gui
import sys
from home_screen import *

pygame.init()
pygame.mixer.init()

click_sound = set_sounds(0.5, 0.6)
background_picture = resize_img("assets/imgs/background.png",SCREEN_HEIGHT, SCREEN_WIDTH)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CODING RACE")

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")
exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 190, 540), (380, 80)),
        text='Exit',
        manager=manager
    )

exit_button.show()
clock = pygame.time.Clock()


def game_screen():
    while True:
        time_delta = clock.tick(60) / 1000.0

        screen.blit(background_picture, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()
                if event.ui_element == exit_button:
                    pygame.quit()
                    sys.exit()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


