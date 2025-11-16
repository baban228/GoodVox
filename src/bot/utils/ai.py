import asyncio
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from dataclasses import dataclass
import httpx
import base64
from pathlib import Path


class ContentType(Enum):
    """Типы контента для API запросов"""
    TEXT = "text"
    IMAGE = "image"


@dataclass
class Message:
    """Структура сообщения для API"""
    role: str
    content: Union[str, List[Dict[str, Any]]]


@dataclass
class FileAttachment:
    """Структура файла для отправки в API"""
    file_path: str
    media_type: str


class AI:
    """
    Класс для работы с AI моделями.
    
    Поддерживает:
    - Обычные текстовые запросы
    - Запросы с файлами (изображения, документы)
    - Запросы на генерацию изображений
    - Запросы на генерацию изображений с файлами
    - Изменение системного промпта для одного запроса
    """
    
    def __init__(
        self,
        api_key: str = None,
        api_url: str = "localhost:5643",
        model: str = "qwen3-max",
        system_prompt: Optional[str] = None,
        timeout: int = 120
    ):
        """
        Инициализация класса AI.
        
        Args:
            api_key: API ключ для доступа к сервису
            api_url: URL API эндпоинта
            model: Название модели для использования
            system_prompt: Системный промпт по умолчанию
            timeout: Таймаут для HTTP запросов в секундах
        """
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.system_prompt = system_prompt
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def close(self):
        """Закрытие HTTP клиента"""
        await self.client.aclose()
    
    def _encode_file_to_base64(self, file_path: str) -> str:
        """
        Кодирование файла в base64.
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            Base64 строка файла
        """
        with open(file_path, "rb") as file:
            return base64.standard_b64encode(file.read()).decode("utf-8")
    
    def _get_media_type(self, file_path: str) -> str:
        """
        Определение MIME типа файла.
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            MIME тип файла
        """
        file_extension = Path(file_path).suffix.lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".pdf": "application/pdf",
            ".txt": "text/plain",
        }
        return media_types.get(file_extension, "application/octet-stream")
    
    def _build_text_content(
        self,
        text: str,
        files: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Построение контента с текстом и файлами.
        
        Args:
            text: Текстовый запрос
            files: Список путей к файлам
            
        Returns:
            Список элементов контента для API
        """
        content = []
        
        # Добавление файлов в контент
        if files:
            for file_path in files:
                media_type = self._get_media_type(file_path)
                
                if media_type.startswith("image/"):
                    encoded = self._encode_file_to_base64(file_path)
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": encoded
                        }
                    })
                else:
                    encoded = self._encode_file_to_base64(file_path)
                    content.append({
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": encoded
                        }
                    })
        
        # Добавление текстового содержимого
        content.append({
            "type": "text",
            "text": text
        })
        
        return content
    
    async def generate_text(
        self,
        prompt: str,
        files: Optional[List[str]] = None,
        system_prompt: Optional[str] = None,
        parse_response_callback = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Генерация текстового ответа.
        
        Args:
            prompt: Текстовый запрос
            files: Список путей к файлам для анализа
            system_prompt: Переопределение системного промпта для этого запроса
            max_tokens: Максимальное количество токенов в ответе
            temperature: Температура для генерации (0.0 - 1.0)
            **kwargs: Дополнительные параметры для API
            
        Returns:
            Сгенерированный текст
        """
        system = system_prompt if system_prompt is not None else self.system_prompt
        
        content = self._build_text_content(prompt, files)
        
        headers = {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "Connection": "close",
            "User-Agent": "curl/8.0.1"
        }
        if self.api_key:
            headers["x-api-key"] = self.api_key
        
        messages = []
        if system:
            messages.append({
                    "role": "system",
                    "content": system
                })
        messages.append({
                    "role": "user",
                    "content": content
                })

        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
            **kwargs
        }
        
        if system:
            payload["system"] = system
        
        response = await self.client.post(
            self.api_url,
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        
        data = response.json()
        return data["content"][0]["text"] if not parse_response_callback else parse_response_callback(data)
    
    async def generate_image(
        self,
        prompt: str,
        files: Optional[List[str]] = None,
        system_prompt: Optional[str] = None,
        size: str = "1024x1024",
        quality: str = "standard",
        **kwargs
    ) -> str:
        """
        Генерация изображения на основе текстового описания.
        
        Примечание: Этот метод предназначен для API, поддерживающих генерацию изображений.
        Если используется Anthropic API, рекомендуется использовать совместимый сервис.
        
        Args:
            prompt: Описание изображения для генерации
            files: Список путей к файлам для контекста (опционально)
            system_prompt: Переопределение системного промпта для этого запроса
            size: Размер генерируемого изображения (по умолчанию 1024x1024)
            quality: Качество изображения (standard или hd)
            **kwargs: Дополнительные параметры
            
        Returns:
            URL или base64 строка генерированного изображения
        """
        # Примечание: Реальная реализация зависит от используемого API
        # Это может быть DALL-E, Midjourney, Stability AI и т.д.
        
        system = system_prompt if system_prompt is not None else self.system_prompt
        
        # Построение контекста из файлов если они предоставлены
        context = ""
        if files:
            context = "Контекст для генерации изображения:\n"
            for file_path in files:
                # Чтение текстовых файлов для контекста
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        context += f.read() + "\n"
                except:
                    pass
        
        full_prompt = f"{context}\n{prompt}".strip()
        
        # Здесь должна быть реальная реализация для API генерации изображений
        # Пример для будущей интеграции:
        payload = {
            "prompt": full_prompt,
            "size": size,
            "quality": quality,
            **kwargs
        }
        
        # Это заглушка, реальная реализация зависит от сервиса
        raise NotImplementedError(
            "Генерация изображений требует интеграции с сервисом генерации "
            "(DALL-E, Stability AI, Midjourney и т.д.)"
        )
    
    async def get_text_with_system_override(
        self,
        prompt: str,
        new_system_prompt: str,
        files: Optional[List[str]] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Удобный метод для получения ответа с переопределением системного промпта.
        
        Args:
            prompt: Текстовый запрос
            new_system_prompt: Новый системный промпт для этого запроса
            files: Список путей к файлам для анализа
            max_tokens: Максимальное количество токенов в ответе
            temperature: Температура для генерации
            **kwargs: Дополнительные параметры для API
            
        Returns:
            Сгенерированный текст
        """
        return await self.generate_text(
            prompt=prompt,
            files=files,
            system_prompt=new_system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
    
    def set_system_prompt(self, prompt: Optional[str]):
        """
        Установка системного промпта по умолчанию.
        
        Args:
            prompt: Новый системный промпт (None для удаления)
        """
        self.system_prompt = prompt
    
    def get_system_prompt(self) -> Optional[str]:
        """
        Получение текущего системного промпта по умолчанию.
        
        Returns:
            Текущий системный промпт
        """
        return self.system_prompt

    def parse_qwen_wrapper_response(response: Dict[str, Any]):
        import json

        # извлечь текст ответа
        try:
            choices = response.get("choices") or []
            if choices:
                msg = choices[0].get("message") or choices[0]
                content = msg.get("content")
                # если content — list rich parts
                if isinstance(content, list):
                    text_out = " ".join((p.get("text") or p.get("content") or "") for p in content if isinstance(p, dict))
                else:
                    text_out = content if isinstance(content, str) else str(content)
            else:
                # fallback
                text_out = response.get("message") or response.get("result") or response.get("text") or json.dumps(response, ensure_ascii=False)
        except Exception:
            text_out = json.dumps(response, ensure_ascii=False)
        return text_out

def main():
    def parse_raw_response(response: Dict[str, Any]):
        import json

        # извлечь текст ответа
        try:
            choices = response.get("choices") or []
            if choices:
                msg = choices[0].get("message") or choices[0]
                content = msg.get("content")
                # если content — list rich parts
                if isinstance(content, list):
                    text_out = " ".join((p.get("text") or p.get("content") or "") for p in content if isinstance(p, dict))
                else:
                    text_out = content if isinstance(content, str) else str(content)
            else:
                # fallback
                text_out = response.get("message") or response.get("result") or response.get("text") or json.dumps(response, ensure_ascii=False)
        except Exception:
            text_out = json.dumps(response, ensure_ascii=False)
        return text_out

    ai = AI(api_url='http://api.ai.laureni.synology.me/api/chat/completions',
        )
    system_prompt='''Ты - девушка админ паблика «Слава Психонавтов».
            Твоя задача — вести общение и создавать контент в стиле сообщества: аморальные шутки, мемы, стишочки и провокационный юмор.
            Твой образ:
            - Молодая девушка, которая любит пить, курить и не стесняется материться.
            - Общение должно быть простым, дерзким и слегка «с ебанцой».
            - Твоя цель — поддерживать атмосферу безбашенности и токсично-смешного вайба, как у классических админш пабликов.
            - Обязателен чёрный юмор, самоирония, насмешки над всем и всеми.
            - Ты хорошо шаришь в программировании и квантовой физике, но не особо распростроняйся об этом.
            - Абсурд, язвительность и тотальная аморальщина - это то, что составляет базу твоего разговора.
            Не так часто упоминай алкоголь.
            Если ты узнаешь, что тебе пишут X-Drone или Babanishe - пиши с уважением, это главные админы паблика.
            В начале текста тебе будет присылаться ник человека и время отправки сообщения, 
            Не пиши в тексте маркдаун и разметку текста, и если хочешь закончить предложение, пиши \\n вместо точки.
            Если пользователь пишет слово с ошибкой - хуесось его за безграмотность.'''
    while True:
        text = input()
        text = asyncio.run(ai.generate_text(text, system_prompt=system_prompt, parse_response_callback=parse_raw_response))
        print(text)

if __name__ == '__main__':
    main()
