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
        self.correct_answer_index = 0
        self.answer_select_buttons = []
        self.users_elements = []
        self.user_form_elements = []

        # Główne przyciski menu
        self.btn_questions = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(250, 180, 300, 75),
            text="Zarządzaj pytaniami",
            manager=manager,
            object_id="#dmin_button"
        )

        self.btn_users = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(250, 280, 300, 75),
            text="Zarządzaj użytkownikami",
            manager=manager,
        )

        self.btn_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(250, 400, 150, 65),
            text="Powrót",
            manager=manager,
        )

        # Listy elementów GUI
        self.questions_elements = []  # Elementy listy pytań
        self.form_elements = []       # Elementy formularza edycji pytania
        
        # Zmienne stanu
        self.current_question_index = -1
        self.current_user_index = -1
        self.questions = self.load_questions()
        self.users = self.load_users()
        
        # Inicjalizacja panelu pytań
        self.create_questions_panel()
        
        # Ukryj elementy pytań na starcie
        self.hide_questions_panel()

    def load_questions(self):
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
            # Ukryj główne przyciski
            self.btn_questions.hide()
            self.btn_users.hide()
            self.btn_back.hide()

            # Pokaż elementy panelu pytań
            for element in self.questions_elements:
                element.show()
                
            self.refresh_questions_list()
        except Exception as e:
            print(f"Błąd w show_questions_panel: {e}")
            traceback.print_exc()
    def show_users_panel(self):
        try:
            self.current_section = "users"
            self.btn_questions.hide()
            self.btn_users.hide()
            self.btn_back.hide()

            self.create_users_panel()
            self.refresh_users_list()
        except Exception as e:
            print(f"Błąd w show_users_panel: {e}")
    def create_users_panel(self):
        if self.users_elements:
            for element in self.users_elements + self.user_form_elements:
                element.show()
            return

        # Lista użytkowników
        self.users_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(20, 40, 450, 600),
            item_list=[],
            manager=self.manager,
        )
        self.users_elements.append(self.users_list)

        # Przycisk dodawania
        self.btn_add_user = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(500, 40, 40, 40),
            text="+",
            manager=self.manager,
        )
        self.users_elements.append(self.btn_add_user)

        # Przycisk powrotu
        self.btn_back_users_panel = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(100, 650, 100, 40),
            text="Powrót",
            manager=self.manager,
        )
        self.users_elements.append(self.btn_back_users_panel)

        # Formularz edycji użytkownika
        y_pos = 100
        self.user_login = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(500, y_pos, 300, 40),
            placeholder_text="Login...",
            manager=self.manager,
        )
        self.user_form_elements.append(self.user_login)

        y_pos += 60
        self.user_password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(500, y_pos, 300, 40),
            placeholder_text="Hasło...",
            manager=self.manager,
        )
        self.user_form_elements.append(self.user_password)

        y_pos += 60
        self.btn_save_user = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(500, y_pos, 120, 40),
            text="Zapisz",
            manager=self.manager,
        )
        self.user_form_elements.append(self.btn_save_user)

        self.btn_delete_user = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(640, y_pos, 120, 40),
            text="Usuń",
            manager=self.manager,
        )
        self.user_form_elements.append(self.btn_delete_user)

        self.btn_cancel_user = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(780, y_pos, 120, 40),
            text="Anuluj",
            manager=self.manager,
        )
        self.user_form_elements.append(self.btn_cancel_user)

        # Ukryj formularz na start
        for element in self.user_form_elements:
            element.hide()        
    def hide_users_panel(self):
        for element in self.users_elements + self.user_form_elements:
            element.hide()

        self.btn_questions.show()
        self.btn_users.show()
        self.btn_back.show()
        self.current_section = None
    def refresh_users_list(self):
        student_titles = []
        self.visible_student_indices = []  # <== Dodaj to przed pętlą
        for idx, user in enumerate(self.users):
            if user.get("role") == "student":
                student_titles.append(f"{len(self.visible_student_indices) + 1}. {user.get('login', '[Brak loginu]')}")
                self.visible_student_indices.append(idx)  # <== I to w środku pętli
        self.users_list.set_item_list(student_titles)
    def load_user_to_form(self):
        if self.current_user_index < 0 or self.current_user_index >= len(self.users):
            return
        user = self.users[self.current_user_index]
        self.user_login.set_text(user.get("login", ""))
        self.user_password.set_text(user.get("password", ""))

        for element in self.user_form_elements:
            element.show()   
    def clear_user_form(self):
        self.user_login.set_text("")
        self.user_password.set_text("")
        for element in self.user_form_elements:
            element.show()
    def save_users_to_file(self):
        try:
            with open("users.json", "w", encoding="utf-8") as file:
                json.dump({"users": self.users}, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Błąd podczas zapisu użytkowników: {e}")        
    def hide_questions_panel(self):
        # Ukryj wszystkie elementy pytań
        for element in self.questions_elements:
            element.hide()
            
        # Ukryj formularz
        for element in self.form_elements:
            element.hide()
            
        # Pokaż główne przyciski
        self.btn_questions.show()
        self.btn_users.show()
        self.btn_back.show()
        self.current_section = None

    def create_questions_panel(self):
        try:
            # Lista pytań
            titles = self.get_questions_titles() if self.questions else ["Brak pytań"]
            self.questions_list = pygame_gui.elements.UISelectionList(
                relative_rect=pygame.Rect(20, 40, 450, 600),
                item_list=titles,
                manager=self.manager,
            )
            self.questions_elements.append(self.questions_list)

            # Przycisk dodaj pytanie
            self.btn_add_question = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(500, 40, 40, 40),
                text="+",
                manager=self.manager,
            )
            self.questions_elements.append(self.btn_add_question)

            # Przycisk powrotu
            self.btn_back_questions_panel = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(100, 650, 100, 40),
                text="Powrót",
                manager=self.manager,
            )
            self.questions_elements.append(self.btn_back_questions_panel)

            # Formularz edycji pytania
            y_pos = 40
            self.question_text = pygame_gui.elements.UITextEntryBox(
                relative_rect=pygame.Rect(500, y_pos, 380, 100),
                placeholder_text="Treść pytania...",
                manager=self.manager,
            )
            self.form_elements.append(self.question_text)

            self.answer_fields = []
            for i in range(4):
                y_pos += 110 if i == 0 else 40
                field = pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect(500, y_pos, 300, 30),
                    placeholder_text=f"Odpowiedź {i + 1}...",
                    manager=self.manager,
                )
                self.answer_fields.append(field)
                self.form_elements.append(field)

                select_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(820, y_pos, 50, 30),
                    text="",
                    manager=self.manager,
                )
                self.answer_select_buttons.append(select_button)
                self.form_elements.append(select_button)

            y_pos += 50
            self.btn_save_question = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(500, y_pos, 120, 40),
                text="Zapisz",
                manager=self.manager,
            )
            self.form_elements.append(self.btn_save_question)

            self.btn_delete_question = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(640, y_pos, 120, 40),
                text="Usuń",
                manager=self.manager,
            )
            self.form_elements.append(self.btn_delete_question)

            self.btn_back_questions = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(780, y_pos, 120, 40),
                text="Anuluj",
                manager=self.manager,
            )
            self.form_elements.append(self.btn_back_questions)

            # Na starcie ukryj formularz
            for element in self.form_elements:
                element.hide()

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
                    elif event.ui_element == self.btn_back_questions_panel:
                        self.hide_questions_panel()
                    elif event.ui_element == self.btn_add_question:
                        self.current_question_index = -1
                        self.clear_question_form()
                        for element in self.form_elements:
                            element.show()
                    elif event.ui_element == self.btn_save_question:
                        self.save_question()
                        for element in self.form_elements:
                            element.hide()
                    elif event.ui_element == self.btn_delete_question:
                        self.delete_question()
                        for element in self.form_elements:
                            element.hide()
                    elif event.ui_element == self.btn_back_questions:
                        for element in self.form_elements:
                            element.hide()
                    elif event.ui_element in self.answer_select_buttons:
                        index = self.answer_select_buttons.index(event.ui_element)
                        self.correct_answer_index = index
                        self.update_correct_answer_buttons()
                    elif event.ui_element == self.btn_back_users_panel:
                        self.hide_users_panel()
                    elif event.ui_element == self.btn_add_user:
                        self.current_user_index = -1
                        self.clear_user_form()
                    elif event.ui_element == self.btn_save_user:
                        self.save_user()
                        self.refresh_users_list()
                        for element in self.user_form_elements:
                            element.hide()
                    elif event.ui_element == self.btn_delete_user:
                        self.delete_user()
                        self.refresh_users_list()
                        for element in self.user_form_elements:
                            element.hide()
                    elif event.ui_element == self.btn_cancel_user:
                        for element in self.user_form_elements:
                            element.hide()

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
                                    for element in self.form_elements:
                                        element.show()
                        except Exception as e:
                            print(f"Błąd ładowania pytania: {e}")

                    elif event.ui_element == self.users_list:
                        try:
                            idx_str = event.text.split('.')[0]
                            if idx_str.isdigit():
                                selected_idx = int(idx_str) - 1
                                if 0 <= selected_idx < len(self.visible_student_indices):
                                    self.current_user_index = self.visible_student_indices[selected_idx]
                                    self.load_user_to_form()
                        except Exception as e:
                            print(f"Błąd ładowania użytkownika: {e}")

        except Exception as e:
            print(f"Błąd w handle_events: {e}")

    def save_user(self):
        login = self.user_login.get_text().strip()
        password = self.user_password.get_text().strip()

        if not login or not password:
            print("Login i hasło nie mogą być puste!")
            return

        if self.current_user_index == -1:
            self.users.append({"login": login, "password": password, "role": "student"})
        else:
            if 0 <= self.current_user_index < len(self.users):
                self.users[self.current_user_index]["login"] = login
                self.users[self.current_user_index]["password"] = password

        self.save_users_to_file()

    def delete_user(self):
        if 0 <= self.current_user_index < len(self.users):
            del self.users[self.current_user_index]
            self.current_user_index = -1
            self.save_users_to_file()
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

        except Exception as e:
            print(f"Błąd w save_question: {e}")

    def delete_question(self):
        try:
            if 0 <= self.current_question_index < len(self.questions):
                del self.questions[self.current_question_index]
                self.save_questions_to_file()
                self.refresh_questions_list()
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
    background_image = pygame.image.load("assets/imgs/background.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    logo_image = pygame.image.load("assets/imgs/logo.png").convert_alpha()
    logo_image = pygame.transform.scale(logo_image, (350, 350))
    running = True
    
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            admin_panel.handle_events(event)
            manager.process_events(event)

        # Rysowanie tła
        screen.blit(background_image, (0, 0))
        
        # Mgiełka
        fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fog_surface.set_alpha(120)
        fog_surface.fill((200, 200, 200))
        screen.blit(fog_surface, (0, 0))
        if admin_panel.current_section != "questions":
            
        # Logo z cieniem
            shadow_offset = 30
            shadow = pygame.Surface((350, 350), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 100))
            
            # Pozycja logo (prawe górne ramię z lekkim marginesem)
            logo_x = SCREEN_WIDTH - 590
            logo_y = 120
            
            # Rysowanie cienia i logo
            screen.blit(shadow, (logo_x + shadow_offset, logo_y + shadow_offset))
            screen.blit(logo_image, (logo_x, logo_y))
        
        # Aktualizacja i rysowanie GUI
        manager.update(time_delta)
        manager.draw_ui(screen)
        
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()