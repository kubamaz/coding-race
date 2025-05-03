import pygame

from home_screen import *
import sys
import random
from Answer_screen import *

#TODO : Shadows
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


pygame.init()
pygame.mixer.init()


click_sound = set_sounds(0.5, 0.6)
background_picture = resize_img("assets/imgs/Question_background.png",SCREEN_HEIGHT, SCREEN_WIDTH)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CODING RACE")

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")


question_title = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0, -300), (700, 110)),
        text='Pytanie ' + str(POINTS + 1),
        manager=manager,
        object_id='#Question_title',
        anchors={'center': 'center'}
    )

OK_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 + 300, 720), (200, 80)),
        text="OK",
        manager=manager
    )




clock = pygame.time.Clock()
questions = import_questions("Questions")

#WERSJA BEZ CZASU NA ODPOWIEDZ NA PYTANIE
def question_screen():
    # Losuje pytanie i wybieram prawidlowa odpowiedz
    question = random.choice(questions)
    while question in answered_questions:
        question = random.choice(questions)

    answered_questions.append(question)
    answers = question[1]
    correct_answer = answers[question[2]]
    # Ustawiam guziki i pytanie

    question_text = pygame_gui.elements.UILabel(

        relative_rect=pygame.Rect((0, -210), (700, 80)),
        text=question[0],
        manager=manager,
        object_id='#Question_text',
        anchors={'center': 'center'}
    )

    answer1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, 300), (500, 80)),
        text="A. " + answers[0],
        manager=manager
    )

    answer2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, 400), (500, 80)),
        text="B. " + answers[1],
        manager=manager
    )

    answer3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, 500), (500, 80)),
        text="C. " + answers[2],
        manager=manager
    )

    answers_button = [answer1, answer2, answer3]

    if len(answers) == 4:
        answer4 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 250, 600), (500, 80)),
            text="D. " + answers[3],
            manager=manager
        )
        answers_button.append(answer4)

    selected_answer = answer1.text[3:]
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.blit(background_picture, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()

                if event.ui_element == OK_button:
                    if selected_answer == correct_answer:
                        answer_screen(True)
                    else:
                        answer_screen(False)
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


question_screen()
