from src.bot.utils.ai import AI

class Info_of_nko:
    def __init__(self):
        # Словарь: user_id -> список собранных строк, позже заменим на бд
        self._collections = {}
        self.ai_recicled = ''

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

    def get_info_as_string(self, user_id: int) -> str:
        """Преобразует список информации пользователя в строку с разделением через точку"""
        info_list = self.get_info(user_id)
        if info_list:
            return ". ".join(info_list) + "."
        return ""
    
    async def recicle_by_ai(self) -> str:
        ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions',
            system_prompt='''Ты — пользователь интеллектуального бота-помощника для канала некоммерческой организации (НКО).
Твоя задача — создавать посты для этого канала.''')
        self.ai_recicled = await ai.generate_text(
            f'''Ты — пользователь. Твоя задача — объяснить боту твою некоммерческую организацию(НКО): {self.get_info_as_string()}''',
                                            parse_response_callback=ai.parse_qwen_wrapper_response)
        
        return self.ai_recicled

# Глобальный экземпляр
info_storage = Info_of_nko()