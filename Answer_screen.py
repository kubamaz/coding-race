from home_screen import *
import sys

#TODO : Shadows

pygame.init()
pygame.mixer.init()


click_sound = set_sounds(0.5, 0.6)
background_picture = resize_img("assets/imgs/Question_background.png",SCREEN_HEIGHT, SCREEN_WIDTH)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CODING RACE")

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")


clock = pygame.time.Clock()

#WERSJA BEZ CZASU NA ODPOWIEDZ NA PYTANIE
def answer_screen(correct):
    t = 3
    if correct:
        txt = "POPRAWNA"
    else:
        txt = "BŁĘDNA"

    Title1 = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0, -120), (800,100)),
        text=txt,
        manager=manager,
        object_id="#Question_title",
        anchors={'center': 'center'},
    )

    Title2 = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((5, -40), (800, 100)),
        text="ODPOWIEDŹ!",
        manager=manager,
        object_id="#Question_title",
        anchors={'center': 'center'},
    )


    Information = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0, 40), (800, 150)),
        manager=manager,
        text="WZNOWIENIE WYSCIGU ZA",
        anchors={'center': 'center'},
        object_id="#Information"
    )

    Information2 = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0, 100), (500, 150)),
        manager=manager,
        text=str(t) + "...",
        anchors={'center': 'center'},
        object_id="#Information"
    )

    start_time = pygame.time.get_ticks()

    while True:
        time_delta = clock.tick(60) / 1000.0
        screen.blit(background_picture, (0, 0))

        current_time = pygame.time.get_ticks()



        if current_time - start_time >= 1000:
            start_time = current_time
            t -= 1
            if t == -1:
                break
            else:
                Information2.text = str(t) + "..."
                Information2.rebuild()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


answer_screen(0)