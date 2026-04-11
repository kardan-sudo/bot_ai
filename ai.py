import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")


class Client:
    def __init__(self, role = None, thinking_level = None):
        """Метод для создания объекта класса клиента. Задается роль и уровень размышления"""
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.role = role
        self.thinking_level = thinking_level
        self.current_chat = None

    def create_chat(self):
        """Метод для создания нового чата"""
        self.current_chat = self.client.chats.create(model='gemini-2.5-flash')

    def drop_chat(self):
        """Метод для удаления чата"""
        self.current_chat = None
    
    def send_message(self, text):
        """Отправляет сообщение в сохраненный чат"""         
        response_model = self.current_chat.send_message_stream(message=text, 
                                                        config=types.GenerateContentConfig(system_instruction=self.role, 
                                                        thinking_config=types.ThinkingConfig(thinking_level=self.thinking_level)))
        response = ''
        for chunk in response_model:
            response += chunk.text
        print(response)
        return response
        


bot = Client()
bot.send_message("Привет! Кто ты? 12341")
bot.send_message("Какую цифру я тебе говорил?")