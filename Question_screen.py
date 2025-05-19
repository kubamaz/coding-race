from common_fun import *
from Answer_screen import answer_screen
import random

#MAX DLUGOSC PYTANIA WYNOSI 69 znakow
def import_questions(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        file_questions = f.read().strip().split('---')
    questions = []
    for part in file_questions:
        line = part.strip().split('\n')
        question = line[0]
        answers = line[1:len(line) - 1]
        ind_correct_answer = int(line[len(line) - 1]) - 1 #indeks poprawnej odpowiedzi
        questions.append((question,answers,ind_correct_answer))
    return questions


background_picture = resize_img("assets/imgs/Question_background.png",SCREEN_HEIGHT, SCREEN_WIDTH)

question_title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, -300), (700, 110)),
        text='Pytanie ' + str(POINTS + 1),
        manager=manager,
        object_id='#Question_title',
        anchors={'center': 'center'}
    )

ok_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 + 300, 720), (200, 80)),
        text="OK",
        manager=manager
    )



question_title.hide()
ok_button.hide()


clock = pygame.time.Clock()
questions = import_questions("Questions")

#WERSJA BEZ CZASU NA ODPOWIEDZ NA PYTANIE
def question_screen():
    if_correct = False
    time = 15 #CZAS TO 15 SEKUND
    start_time = pygame.time.get_ticks()
    time_information = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, -370), (700, 110)),
        text='Czas : ' + str(time) + ' sekund',
        manager=manager,
        object_id='#time',
        anchors={'center': 'center'}
    )
    
    # Losuje pytanie i wybieram prawidlowa odpowiedz
    question = random.choice(questions)
    while question in answered_questions:
        question = random.choice(questions)

    answered_questions.append(question)
    answers = question[1]
    correct_answer = answers[question[2]]
    # Ustawiam guziki i pytanie

    question_text = pygame_gui.elements.UITextBox(

        relative_rect=pygame.Rect((0, -80), (SCREEN_WIDTH - 200, 300)),
        html_text="<shadow size=1 offset=1,1 color=#000000>"+question[0]+"</shadow>",
        manager=manager,
        anchors={'center': 'center'}
    )

    answer1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, 350), (500, 80)),
        text="A. " + answers[0],
        manager=manager
    )

    answer2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, 450), (500, 80)),
        text="B. " + answers[1],
        manager=manager
    )

    answer3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, 550), (500, 80)),
        text="C. " + answers[2],
        manager=manager
    )

    answers_button = [answer1, answer2, answer3]

    if len(answers) == 4:
        answer4 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, 650), (500, 80)),
            text="D. " + answers[3],
            manager=manager
        )
        answers_button.append(answer4)

    selected_answer = 'Brak'
    running = True
    while running:
        #ODLICZAM CZAS
        current_time = pygame.time.get_ticks()

        if current_time - start_time >= 1000:
            start_time = current_time
            time -= 1
        if time == -1:
            time_information.hide()
            question_text.hide()
            question_title.hide()
            ok_button.hide()
            answer1.hide()
            answer2.hide()
            answer3.hide()
            if len(answers) == 4:
                answer4.hide()
            if selected_answer == correct_answer:
                answer_screen(1)
            elif selected_answer == 'Brak':
                answer_screen(2)
            else:
                answer_screen(0)
            break
        else:
            time_information.text = 'Czas  : ' + str(time) + ' sekund'
            time_information.rebuild()
        
        time_delta = clock.tick(60) / 1000.0
        screen.blit(background_picture, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()
                ok_button.show()
                if event.ui_element == ok_button:
                    time_information.hide()
                    question_text.hide()
                    question_title.hide()
                    ok_button.hide()
                    answer1.hide()
                    answer2.hide()
                    answer3.hide()
                    if len(answers) == 4:
                        answer4.hide()
                    if selected_answer == correct_answer:
                        if_correct = True
                        answer_screen(1)
                    else:
                        answer_screen(0)
                    running = False

                    

                for button in answers_button:
                    if button.colours['normal_border'] != pygame.Color("#AE0909"):
                        button.colours['normal_border'] = pygame.Color("#AE0909")
                        button.colours['hovered_text'] = pygame.Color("#FFFFFF")
                        button.rebuild()

                event.ui_element.colours['normal_border'] = pygame.Color("#FF4500")
                event.ui_element.colours['hovered_text'] = pygame.Color("#F56914")
                event.ui_element.rebuild()

                selected_answer = event.ui_element.text[3:]
            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    return if_correct


# question_screen()
