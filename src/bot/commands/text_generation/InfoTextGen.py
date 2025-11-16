from telegram import Update


class InfoTextGen:
    def __init__(self):
        self.questions = {
                            2: "Дата:",
                            3: "Место:",
                            4: "Приглашённые люди:",
                            5: "Доп. детали:"
        }
        self.number_of_question = 1
        self.answers = {}

    def add_answer(self, answer: str):
        self.answers[self.number_of_question] = answer

    def get_question(self):
        self.number_of_question += 1
        return self.questions[self.number_of_question]

    def get_answers(self):
        return self.answers