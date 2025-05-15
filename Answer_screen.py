from common_fun import *


background_picture = resize_img("assets/imgs/Question_background.png",SCREEN_HEIGHT, SCREEN_WIDTH)

def answer_screen(correct):
    t = 3
    if correct:
        txt = "POPRAWNA\nODPOWIEDZ!"
    else:
        txt = "BŁĘDNA\nODPOWIEDZ!"

    summary_text = pygame_gui.elements.UITextBox(

        relative_rect=pygame.Rect((0, -10), (800,400)),
        html_text="<shadow size=3 offset=1,1 color=#000000>"+txt+"</shadow>",
        manager=manager,
        object_id="#summary_answer_text",
        anchors={'center': 'center'}
    )



    information = pygame_gui.elements.UITextBox(

        relative_rect=pygame.Rect((0, 80), (800, 150)),
        html_text="<shadow size=2 offset=1,1 color=#000000>"+"WZNOWIENIE WYSCIGU ZA\n"+str(t)+"..."+"</shadow>",
        manager=manager,
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
                summary_text.hide()
                information.hide()
                
                break
            else:
                information.html_text = "<shadow size=2 offset=1,1 color=#000000>"+"WZNOWIENIE WYSCIGU ZA\n"+str(t)+"..."+"</shadow>"
                information.rebuild()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    summary_text.hide()
    information.hide()
