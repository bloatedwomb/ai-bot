from configuration import TOKEN
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import random

bot = telebot.TeleBot(TOKEN)

url = "https://rb.ru/list/the-most-interesting-neural-networks/"
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

tag_list = soup.find('li', dir="ltr")
raw_names = tag_list.find_all('a', class_="smooth_scroll")[1:-1]
names = [item.find('strong').text for item in raw_names]

links = [
    'https://ya.ru/ai/gpt',
    'https://giga.chat/',
    'https://chatgpt.com/',
    'https://copilot.microsoft.com/',
    'https://gemini.google.com/'
]

descriptions = [
    "Большая языковая модель от Яндекса...",
    "Языковая модель от Сбера...",
    "Одна из самых известных моделей в мире...",
    "Инструмент для помощи разработчикам...",
    "Мультимодальная модель от Google..."
]

ai_data = {
    names[i]: {'url': links[i], 'info': descriptions[i]} for i in range(len(names))
}

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используйте команду /networks для просмотра списка нейросетей.")

@bot.message_handler(commands=["networks"])
def show_networks(message):
    markup = types.InlineKeyboardMarkup()
    for name in names:
        markup.add(types.InlineKeyboardButton(name, callback_data=name))
    markup.add(types.InlineKeyboardButton("Случайная нейросеть", callback_data="random_ai"))
    bot.send_message(message.chat.id, "Выберите нейросеть:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    selected_name = random.choice(names) if call.data == "random_ai" else call.data
    data = ai_data.get(selected_name, {})
    reply = (
        f"Вы выбрали: {selected_name}.\n"
        f"Ссылка: {data.get('url', 'Нет данных')}\n"
        f"Описание: {data.get('info', 'Нет данных')}"
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, reply)
    bot.send_message(call.message.chat.id, "Чтобы выбрать другую нейросеть, введите команду /networks")

bot.polling()