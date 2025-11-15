class Info_setting:
    def __init__(self):
        # Словарь: user_id -> роль ИИ
        self.role_of_ai = {}
        # Словарь: user_id -> цель/желание пользователя
        self.what_you_want = {}

        # Дефолтные значения
        self.default_role = 'default'
        self.default_want = 'default'

    def set_role(self, user_id: int, role: str) -> None:
        """Устанавливает роль ИИ для указанного пользователя."""
        self.role_of_ai[user_id] = role

    def set_what_you_want(self, user_id: int, want: str) -> None:
        """Устанавливает цель/желание пользователя для указанного пользователя."""
        self.what_you_want[user_id] = want

    def get_role(self, user_id: int) -> str:
        """Возвращает роль ИИ для указанного пользователя."""
        return self.role_of_ai.get(user_id, self.default_role)

    def get_what_you_want(self, user_id: int) -> str:
        """Возвращает цель/желание пользователя."""
        return self.what_you_want.get(user_id, self.default_want)

    def clear_user_settings(self, user_id: int) -> None:
        """Очищает настройки для указанного пользователя."""
        if user_id in self.role_of_ai:
            del self.role_of_ai[user_id]
        if user_id in self.what_you_want:
            del self.what_you_want[user_id]

    def get_all_settings(self, user_id: int) -> dict:
        """Возвращает все настройки пользователя в виде словаря."""
        return {
            'role': self.get_role(user_id),
            'want': self.get_what_you_want(user_id)
        }

    def set_default_role(self, default_role: str) -> None:
        """Устанавливает дефолтную роль для всех новых пользователей."""
        self.default_role = default_role

    def set_default_want(self, default_want: str) -> None:
        """Устанавливает дефолтное желание для всех новых пользователей."""
        self.default_want = default_want

    def reset_to_defaults(self, user_id: int) -> None:
        """Сбрасывает настройки пользователя к дефолтным значениям."""
        self.clear_user_settings(user_id)

info_setting = Info_setting()