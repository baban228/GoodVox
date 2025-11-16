class Info_post_gen:
    def __init__(self):
        # Словарь: user_id -> текст для картинки
        self.post_image = {}
        # Словарь: user_id -> текст для текста
        self.post_text = {}

    def add_image(self, user_id: int, _post_image: str):
        if user_id not in self.post_image:
            self.post_image[user_id] = []
        self.post_image[user_id].append(_post_image)

    def add_text(self, user_id: int, _post_text: str):
        if user_id not in self.post_text:
            self.post_text[user_id] = []
        self.post_text[user_id].append(_post_text)

    def get_image(self, user_id: int) -> list:
        """Возвращает список текстов для картинок пользователя"""
        return self.post_image.get(user_id, [])

    def get_text(self, user_id: int) -> list:
        """Возвращает список текстов для постов пользователя"""
        return self.post_text.get(user_id, [])

    def get_all_data(self, user_id: int) -> dict:
        """Возвращает все данные пользователя в виде словаря"""
        return {
            'images': self.get_image(user_id),
            'texts': self.get_text(user_id)
        }
info_post_gen = Info_post_gen()