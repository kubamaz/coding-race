from home_screen import *

def import_questions(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        file_questions = f.read().strip().split('---')
    questions = []
    for part in file_questions:
        line = part.strip().split('\n')
        question = line[0]
        answers = {a for a in line[1:len(line) - 1]}
        ind_correct_answer = int(line[len(line) - 1]) - 1 #indeks poprawnej odpowiedzi
        questions.append((question,answers,ind_correct_answer))
    return questions


q = import_questions("Questions")
print(q)