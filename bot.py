import telebot
import requests
from datetime import datetime

TOKEN = "8825550560:AAGIYVZTCgyffCj3XzBZr3DXkscNniFfyI0"
bot = telebot.TeleBot(TOKEN)
SERVER_URL = "https://server-for-quotes-bot-production.up.railway.app"


@bot.message_handler(commands=['start'])  # стартовая команда
def start(message):
    text = """Привет! я бот для заказов.

Доступные команды:
/add /текст цитаты/автор цытаты- добавить цитату
/quote_random - рандомная цитата
/delete <id> - удалить цитату
/get_quote <id> - получить цитату по id
/get_quotes  - получить цитаты"""

    bot.reply_to(message, text)

@bot.message_handler(commands=['quote_random'])
def quote_random(message):
    try:
        result = []
        response = requests.get(f"{SERVER_URL}/random")
        if response.status_code == 200:
            data = response.json()
            result = data[0]
            if not result:
                bot.reply_to(message, "Цитат пока нет")
                return
        else:
            bot.reply_to(message, "ошибка сервера")
            return
        text = "рандомная цитата\n"
        text += f"id - {result['Id']}\n text - {result['Text']}\n author - {result['Author']}\n Created_at - {result['Created_at']}\n"
        print(text)
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['get_quotes'])
def get_quotes(message):
    try:
        result = []
        response = requests.get(f"{SERVER_URL}/quotes")
        if response.status_code == 200:
            result = response.json()
            if not result:
                bot.reply_to(message, "Цитат пока нет")
                return
        else:
            bot.reply_to(message, "ошибка сервера")
            return
        text = "список цитат:\n"
        for r in result:
            text += f"id - {r['Id']}\n text - {r['Text']}\n author - {r['Author']}\n Created_at - {r['Created_at']}\n"
            print(text)
            bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['get_quote'])
def get_quote(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "data not found")
            return
        try:
            id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "id not integer")
            return
        result = []
        response = requests.get(f"{SERVER_URL}/quote_id?id={id}")
        if response.status_code == 200:
            data = response.json()
            result = data[0]
            if not result:
                bot.reply_to(message, "Цитаты нет")
                return
        else:
            bot.reply_to(message, "ошибка сервера")
            return
        text = "цитата:\n"
        text += f"id - {result['Id']}\n text - {result['Text']}\n author - {result['Author']}\n Created_at - {result['Created_at']}\n"
        print(text)
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['delete'])
def get_quote(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "data not found")
            return
        try:
            id = int(parts[1])
        except ValueError:
            bot.reply_to(message, "id not integer")
            return
        response = requests.get(f"{SERVER_URL}/delete?id={id}")
        if response.status_code == 200:
            bot.reply_to(message, "Цитата удалена")
        else:
            bot.reply_to(message, "ошибка сервера")
            return
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['add'])
def add(message):
    try:
        parts = message.text.split("/")
        if len(parts) < 3:
            bot.reply_to(message, "error, data not found")
            return
        response = requests.get(f"{SERVER_URL}/quote?text={parts[2]}&author={parts[3]}")
        if response.status_code == 200:
            bot.reply_to(message, "Успешно! цитата добавлена")
        else:
            bot.reply_to(message, "ошибка сервера")
            return
    except Exception as e:
        bot.reply_to(message, e)

if __name__ == '__main__':
    bot.infinity_polling()
