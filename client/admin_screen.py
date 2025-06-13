import pygame
import pygame_gui
import json
import os
import traceback

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832

class AdminPanel:
    def __init__(self, screen, manager, back_callback):
        self.screen = screen
        self.manager = manager
        self.back_callback = back_callback
        self.current_section = None
        self.correct_answer_index = 0  # domyślnie pierwsza odpowiedź
        self.answer_select_buttons = []

        self.main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            manager=manager
        )

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

        self.questions_panel = None
        self.users_panel = None
        self.current_question_index = -1
        self.current_user_index = -1
        self.questions = self.load_questions()
        self.users = self.load_users()

    def load_questions(self):
        # Twój kod bez zmian
        questions = []
        try:
            if os.path.exists("Questions"):
                with open("Questions", "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if not content:
                        return questions

                    blocks = content.split("---")
                    for block in blocks:
                        if not block.strip():
                            continue

                        lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
                        if len(lines) < 2:
                            continue

                        question_text = lines[0]
                        answers = []
                        correct_answer = None
                        i = 1

                        while i < len(lines) and lines[i].startswith("Odp"):
                            answer = lines[i].split(' ', 1)[-1].strip()
                            answers.append(answer)
                            i += 1

                        if i < len(lines) and lines[i].isdigit():
                            correct_answer = int(lines[i])
                            i += 1

                        if correct_answer is None or correct_answer < 1 or correct_answer > len(answers):
                            correct_answer = 1 if answers else 0

                        if len(answers) >= 2:
                            questions.append({
                                "text": question_text,
                                "answers": answers,
                                "correct": correct_answer
                            })
        except Exception as e:
            print(f"Błąd wczytywania pytań: {e}")
            traceback.print_exc()

        return questions

    def load_users(self):
        try:
            if os.path.exists("users.json"):
                with open("users.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    return data.get("users", [])
        except Exception as e:
            print(f"Błąd wczytywania użytkowników: {e}")
        return []

    def show_questions_panel(self):
        try:
            self.current_section = "questions"
            self.main_panel.hide()

            if self.questions_panel is None:
                self.create_questions_panel()
            else:
                self.questions_panel.show()
                self.refresh_questions_list()
        except Exception as e:
            print(f"Błąd w show_questions_panel: {e}")
            traceback.print_exc()

    def create_questions_panel(self):
        try:
            self.questions_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
                manager=self.manager
            )

            titles = self.get_questions_titles() if self.questions else ["Brak pytań"]

            self.questions_list = pygame_gui.elements.UISelectionList(
                relative_rect=pygame.Rect(20, 20, 300, 500),
                item_list=titles,
                manager=self.manager,
                container=self.questions_panel
            )

            self.btn_add_question = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(330, 20, 40, 40),
                text="+",
                manager=self.manager,
                container=self.questions_panel
            )

            self.question_form_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(380, 20, 400, 560),
                manager=self.manager,
                container=self.questions_panel
            )

            y_pos = 20
            self.question_text = pygame_gui.elements.UITextEntryBox(
                relative_rect=pygame.Rect(10, y_pos, 380, 100),
                placeholder_text="Treść pytania...",
                manager=self.manager,
                container=self.question_form_panel
            )

            self.answer_fields = []
            for i in range(4):
                y_pos += 110 if i == 0 else 40
                field = pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect(10, y_pos, 300, 30),
                    placeholder_text=f"Odpowiedź {i + 1}...",
                    manager=self.manager,
                    container=self.question_form_panel
                )
                self.answer_fields.append(field)

                select_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(320, y_pos, 50, 30),
                    text="",
                    manager=self.manager,
                    container=self.question_form_panel
                )
                self.answer_select_buttons.append(select_button)

            y_pos += 50
            self.btn_save_question = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(10, y_pos, 120, 40),
                text="Zapisz",
                manager=self.manager,
                container=self.question_form_panel
            )

            self.btn_delete_question = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(140, y_pos, 120, 40),
                text="Usuń",
                manager=self.manager,
                container=self.question_form_panel
            )

            self.btn_back_questions = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(270, y_pos, 120, 40),
                text="Anuluj",
                manager=self.manager,
                container=self.question_form_panel
            )

            self.question_form_panel.hide()
        except Exception as e:
            print(f"Błąd w create_questions_panel: {e}")
            traceback.print_exc()

    def refresh_questions_list(self):
        try:
            titles = self.get_questions_titles() if self.questions else ["Brak pytań"]
            self.questions_list.set_item_list(titles)
        except Exception as e:
            print(f"Błąd w refresh_questions_list: {e}")

    def get_questions_titles(self):
        titles = []
        for idx, q in enumerate(self.questions):
            try:
                text = q.get("text", "[Brak treści pytania]")
                if len(text) > 30:
                    title = f"{idx + 1}. {text[:30]}..."
                else:
                    title = f"{idx + 1}. {text}"
                titles.append(title)
            except Exception as e:
                print(f"Błąd przetwarzania pytania {idx}: {e}")
                titles.append(f"{idx + 1}. [BŁĄD]")
        return titles

    def handle_events(self, event):
        try:
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.btn_questions:
                        self.show_questions_panel()
                    elif event.ui_element == self.btn_users:
                        self.show_users_panel()
                    elif event.ui_element == self.btn_back:
                        self.back_callback()
                    elif hasattr(self, 'btn_back_users') and event.ui_element == self.btn_back_users:
                        self.users_panel.hide()
                        self.main_panel.show()
                    elif event.ui_element == self.btn_add_question:
                        self.current_question_index = -1
                        self.clear_question_form()
                        self.question_form_panel.show()
                    elif event.ui_element == self.btn_save_question:
                        self.save_question()
                    elif event.ui_element == self.btn_delete_question:
                        self.delete_question()
                    elif event.ui_element == self.btn_back_questions:
                        self.question_form_panel.hide()
                    elif event.ui_element in self.answer_select_buttons:
                        index = self.answer_select_buttons.index(event.ui_element)
                        self.correct_answer_index = index
                        self.update_correct_answer_buttons()
                elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element in self.answer_fields:
                        self.update_correct_answer_buttons()

                elif event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_element == self.questions_list and self.questions:
                        try:
                            idx_str = event.text.split('.')[0]
                            if idx_str.isdigit():
                                self.current_question_index = int(idx_str) - 1
                                if 0 <= self.current_question_index < len(self.questions):
                                    self.load_question_to_form()
                                    self.question_form_panel.show()
                        except Exception as e:
                            print(f"Błąd ładowania pytania: {e}")

        except Exception as e:
            print(f"Błąd w handle_events: {e}")

    def clear_question_form(self):
        self.question_text.set_text("")
        for field in self.answer_fields:
            field.set_text("")
        self.correct_answer_index = 0
        self.update_correct_answer_buttons()

    def load_question_to_form(self):
        try:
            if not self.questions or self.current_question_index < 0:
                return

            question = self.questions[self.current_question_index]
            self.question_text.set_text(question.get("text", ""))

            answers = question.get("answers", [])
            for i, field in enumerate(self.answer_fields):
                if i < len(answers):
                    field.set_text(answers[i])
                else:
                    field.set_text("")

            self.correct_answer_index = question.get("correct", 1) - 1
            self.update_correct_answer_buttons()

        except Exception as e:
            print(f"Błąd w load_question_to_form: {e}")

    def save_question(self):
        try:
            answers = [field.get_text().strip() for field in self.answer_fields]
            non_empty_answers = [ans for ans in answers if ans]

            if len(non_empty_answers) < 3:
                print("Wymagane co najmniej 3 odpowiedzi, aby zapisać pytanie!")
                return

            new_question = {
                "text": self.question_text.get_text(),
                "answers": non_empty_answers,
                "correct": self.correct_answer_index + 1
            }

            if self.current_question_index == -1:
                self.questions.append(new_question)
            else:
                if 0 <= self.current_question_index < len(self.questions):
                    self.questions[self.current_question_index] = new_question

            self.save_questions_to_file()
            self.refresh_questions_list()
            self.question_form_panel.hide()

        except Exception as e:
            print(f"Błąd w save_question: {e}")

    def delete_question(self):
        try:
            if 0 <= self.current_question_index < len(self.questions):
                del self.questions[self.current_question_index]
                self.save_questions_to_file()
                self.refresh_questions_list()
                self.question_form_panel.hide()
        except Exception as e:
            print(f"Błąd w delete_question: {e}")

    def save_questions_to_file(self):
        try:
            with open("Questions", "w", encoding="utf-8") as file:
                for question in self.questions:
                    file.write(question["text"] + "\n")
                    for idx, answer in enumerate(question["answers"]):
                        file.write(f"Odp{idx + 1} {answer}\n")
                    file.write(str(question["correct"]) + "\n")
                    file.write("---\n")
        except Exception as e:
            print(f"Błąd podczas zapisu pytań: {e}")

    def update_correct_answer_buttons(self):
        try:
            non_empty_answers = [field.get_text().strip() for field in self.answer_fields if field.get_text().strip()]
            count = len(non_empty_answers)

            for i, button in enumerate(self.answer_select_buttons):
                answer_text = self.answer_fields[i].get_text().strip()

                if count < 3:
                    button.set_text("")
                    button.disable()
                else:
                    if answer_text == "":
                        button.set_text("")
                        button.disable()
                    else:
                        button.enable()
                        if i == self.correct_answer_index:
                            button.set_text("V")
                        else:
                            button.set_text("")
        except Exception as e:
            print(f"Błąd w update_correct_answer_buttons: {e}")


def back_to_main_menu():
    print("Powrót do menu głównego")


def main():
    pygame.init()
    pygame.display.set_caption("Panel administratora")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

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


if __name__ == "__main__":
    main()
