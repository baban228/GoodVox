class InfoTextGen:
    def __init__(self):
        self.cat: str = ""
        self.first_post_desc: str = ""
        self.current_question: str | None = None
        self.answers: dict[str, str] = {}   # {"ask": "ans"}


    def set_cat(self, cat: str):
        self.cat = cat

    def get_cat(self) -> str:
        return self.cat


    def set_first_post_desc(self, desc: str):
        self.first_post_desc = desc

    def get_first_post_desc(self) -> str:
        return self.first_post_desc


    def add_answer(self, question: str, answer: str):
        """Сохраняет пару вопрос–ответ."""
        if question:
            self.answers[question] = answer

    def get_answers(self) -> dict:
        return self.answers

    def get_answers_as_text(self) -> str:
        """Превращает ответы в читаемый текст для отправки в OpenAI."""
        if not self.answers:
            return "Нет уточняющей информации."
        return "\n".join(f"Q: {q}\nA: {a}\n" for q, a in self.answers.items())


    def set_current_question(self, q: str):
        self.current_question = q

    def get_current_question(self) -> str | None:
        return self.current_question


    def reset(self):
        self.cat = ""
        self.first_post_desc = ""
        self.current_question = None
        self.answers = {}
