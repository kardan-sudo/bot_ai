import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")


#The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GEMINI_API_KEY)

chat = client.chats.create(model='gemini-3-flash-preview')

text = str(input('Запрос:'))

response = chat.send_message_stream(text)
for chunk in response:
    print(chunk.text, end="")