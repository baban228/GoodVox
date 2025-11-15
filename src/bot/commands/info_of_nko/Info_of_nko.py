class Info_of_nko:
    def __init__(self):
        # Словарь: user_id -> список собранных строк, позже заменим на бд
        self._collections = {}

    def add_info(self, user_id: int, text: str) -> None:
        if user_id not in self._collections:
            self._collections[user_id] = []
        self._collections[user_id].append(text)

    def get_info(self, user_id: int) -> list:
        return self._collections.get(user_id, [])

    def clear_info(self, user_id: int) -> None:
        """Очищает информацию для указанного пользователя."""
        if user_id in self._collections:
            del self._collections[user_id]

    def remove_last_entry(self, user_id: int) -> str or None:
        """Удаляет последнюю запись из списка и возвращает её (если есть)."""
        if user_id in self._collections and self._collections[user_id]:
            return self._collections[user_id].pop()

# Глобальный экземпляр
info_storage = Info_of_nko()