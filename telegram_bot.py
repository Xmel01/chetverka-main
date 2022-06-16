import telebot
from telebot import types
import os
import django
from telebot.types import WebAppInfo
import requests, re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'troyka.settings')
django.setup()

from teletroyka.models import TelegramUser

TOKEN = '5311071553:AAGZjGXmV15T6qHP3reVxtIXurDK6Y64sG0'
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['getMe'])
def getMeMessage(message):
    user = bot.get_me()
    bot.reply_to(message, f'Your id is {user}')


def listener(message):
    for m in message:
        if m.text not in ['/start', '/getMe', 'Информация']:
            bot.send_message(m.chat.id, "Я не знаю такой комманды, нажмите 'Информация' для уточнения запроса)")
        elif m.text == '/start':
            URL = 'https://test-bots.sbertroika.tech/base/'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            itembtn1 = types.KeyboardButton('Купить билет',web_app=WebAppInfo(url=URL,))
            itembtn2 = types.KeyboardButton('Информация')
            menu_button = types.MenuButtonWebApp('web_app', 'Билеты', web_app=WebAppInfo(url = URL))
            bot.set_chat_menu_button(m.chat.id, menu_button)
            keyboard.add(itembtn1, itembtn2)
            users = TelegramUser.objects.filter(telegram_user_id=f'{m.from_user.id}')
            if users.count() == 0:
                new_user = TelegramUser.objects.create(telegram_user_id=f'{m.from_user.id}',
                                            telegram_user_first_name=f'{m.from_user.first_name}',
                                            telegram_user_last_name=f'{m.from_user.last_name}',
                                            telegram_user_nickname=f'{m.from_user.username}')
                # data = {'pk': new_user.pk}
                # r = requests.post('http://127.0.0.1:8000/base/payform/', data=data)
                # bot.send_message(m.chat.id, r)
                bot.send_message(m.chat.id, 'Приветствую в TicketBot', reply_markup=keyboard)
            else:
                bot.send_message(m.chat.id, f'Приветствую, {m.from_user.first_name}', reply_markup=keyboard)
                # data = {'pk': users[0].pk}
                # r = requests.post('http://127.0.0.1:8000/base/payform/', data=data)
                # bot.send_message(m.chat.id, r)

        elif m.text == 'Информация':

            bot.send_message(m.chat.id, 'Тут раздел с иноформацией по возможностям бота (попозже доделаю)')



bot.set_update_listener(listener)
bot.polling(none_stop=True)