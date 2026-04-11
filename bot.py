"""Импорты для работы"""
import sys
import os
import asyncio
from telebot.async_telebot import AsyncTeleBot
from ai import fetch_models, TEXT_MODELS_URL, select_model_from_list, generate_text_with_model, IMAGE_MODELS_URL, generate_image_with_model
from button_cancel import CancelKeyboard


TOKEN="Token"

user_states = {}
user_models = {}

bot=AsyncTeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
async def start_message(message):
    """Стартовая функция"""
    user_name = message.from_user.first_name
    hello_text = f"""{user_name} Добро пожаловать в FlyMalysh.ai! \
                     \nКуда вас направить(нажмите на команду)? \n1. Генерация текста --- /text \
                         \n2. Генерация фотографии --- /photo \n"""
    await bot.send_message(message.chat.id,
                           hello_text)

@bot.message_handler(func=lambda message: message.text.lower() == "отмена ❌")
async def handle_cancel(message):
    """Функция для обработки кнопки 'Отмена', возвращает в начало"""
    await bot.send_message(
        message.chat.id,
        "❌ Действие отменено.",
        reply_markup=CancelKeyboard.remove()
    )
    await bot.send_message(message.chat.id,
                           'Куда вас направить(нажмите на команду)? \n1. Генерация текста --- /text\
                            \n2. Генерация фотографии --- /photo ')
    # Возвращаем в главное меню (или другое состояние)
    del user_states[message.chat.id]["state"]

@bot.message_handler(commands=['text'])
async def view_text_model(message):
    """Функция для работы с текстом"""  
    user_states[message.chat.id] = {"state": "wait_number_text_models"}
    text_models = fetch_models(TEXT_MODELS_URL)
    user_models[message.chat.id] = {'models_data' : text_models}
    if text_models:
        selected_text_model_details = select_model_from_list(text_models, "text")
        await bot.send_message(message.chat.id,
                               selected_text_model_details,
                               reply_markup=CancelKeyboard.create())
    else:
        await bot.send_message(message.chat.id,
                               "Не удалось загрузить текстовые модели, попробуйте заново.\
                                \n 'Куда вас направить(нажмите на команду)?\
                               \n1. Генерация текста --- /text \
                                \n2. Генерация фотографии --- /photo",
                                reply_markup=CancelKeyboard.remove())
        del user_states[message.chat.id]["state"]

@bot.message_handler(func=lambda message:
    user_states.get(message.chat.id).get("state") == "wait_number_text_models")
async def select_text_model(message):
    """Функция для выбора текстовой модели"""
    models_data = user_models.get(message.chat.id).get("models_data")
    try:
        choice = int(message.text) - 1
        if 0 <= choice < len(models_data):
            user_states[message.chat.id] = {"state": "work_with_text_models"}
            user_models[message.chat.id] = {"select_model": models_data[choice]}
            msg = f"\nВыбрана модель для текста: {models_data[choice]['name']} \
            ({models_data[choice]['description']}) \
            \n Введите ваш текстовый запрос (или 'отмена' для выхода):"
            await bot.send_message(message.chat.id,
                                   msg,
                                   reply_markup=CancelKeyboard.create())
        else:
            await bot.send_message(message.chat.id,
                                   "Неверный номер. Пожалуйста, попробуйте снова.", 
                                   reply_markup=CancelKeyboard.create())
    except ValueError:
        await bot.send_message(message.chat.id,
                               "Неверный ввод. Пожалуйста, введите число.",
                               reply_markup=CancelKeyboard.create())

@bot.message_handler(func=lambda message:
    user_states.get(message.chat.id).get("state") == "work_with_text_models")
async def work_text_model(message):
    """Фукнция для отправки промтов и получения ответов пользователем"""
    print(f'{message.chat.id} отправил {message.text}')
    selected_text_model_details = user_models.get(message.chat.id).get("select_model")
    if selected_text_model_details:
        await bot.send_message(message.chat.id,
                               'Отправка запроса...', 
                               reply_markup=CancelKeyboard.create())
        await bot.send_message(message.chat.id,
                               generate_text_with_model(selected_text_model_details, message.text),
                               reply_markup=CancelKeyboard.create())
        await bot.send_message(message.chat.id,
                               'Если необходимо отправьте следующий запрос', 
                               reply_markup=CancelKeyboard.create())

@bot.message_handler(commands=['photo'])
async def view_photo_model(message):
    """Функция для работы с изображениями"""  
    user_states[message.chat.id] = {"state": "wait_number_photo_models"}
    photo_models = fetch_models(IMAGE_MODELS_URL)
    user_models[message.chat.id] = {'models_data' : photo_models}
    if photo_models:
        selected_text_model_details = select_model_from_list(photo_models, "image")
        await bot.send_message(message.chat.id,
                               selected_text_model_details,
                               reply_markup=CancelKeyboard.create())
    else:
        await bot.send_message(message.chat.id,
                               "Не удалось загрузить модели для изображений, попробуйте заново.\
                                \n 'Куда вас направить(нажмите на команду)?\
                               \n1. Генерация текста --- /text \
                                \n2. Генерация фотографии --- /photo",
                                reply_markup=CancelKeyboard.remove())
        del user_states[message.chat.id]["state"]

@bot.message_handler(func=lambda message:
    user_states.get(message.chat.id).get("state") == "wait_number_photo_models")
async def select_photo_model(message):
    """Функция для выбора модели для изображений"""
    models_data = user_models.get(message.chat.id).get("models_data")
    print(models_data, type(models_data))
    try:
        choice = int(message.text) - 1
        print(choice)
        if 0 <= choice < len(models_data):
            user_states[message.chat.id] = {"state": "work_with_photo_models"}
            user_models[message.chat.id] = {"select_model": models_data[choice]}
            msg = f"\nВыбрана модель для изображений: {models_data[choice]}\
            \n Введите ваш запрос (или 'отмена' для выхода):"
            await bot.send_message(message.chat.id,
                                   msg,
                                   reply_markup=CancelKeyboard.create())
        else:
            await bot.send_message(message.chat.id,
                                   "Неверный номер. Пожалуйста, попробуйте снова.", 
                                   reply_markup=CancelKeyboard.create())
    except ValueError:
        await bot.send_message(message.chat.id,
                               "Неверный ввод. Пожалуйста, введите число.",
                               reply_markup=CancelKeyboard.create())

@bot.message_handler(func=lambda message:
    user_states.get(message.chat.id).get("state") == "work_with_photo_models")
async def work_photo_model(message):
    """Фукнция для отправки промтов и получения ответов пользователем"""
    print(f'{message.chat.id} отправил {message.text}')
    selected_text_model_details = user_models.get(message.chat.id).get("select_model")
    if selected_text_model_details:
        await bot.send_message(message.chat.id,
                               'Отправка запроса...', 
                               reply_markup=CancelKeyboard.create())
        with open(generate_image_with_model(selected_text_model_details, prompt=message.text), 'rb') as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption="Вот ваше фото! 📸",
                reply_markup=CancelKeyboard.create()
            )

        await bot.send_message(message.chat.id,
                               'Если необходимо отправьте следующий запрос', 
                               reply_markup=CancelKeyboard.create())

asyncio.run(bot.infinity_polling())
