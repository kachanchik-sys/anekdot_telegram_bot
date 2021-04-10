from time import sleep
import telebot
import logging
import os
import requests
import re

# constants
token = ''
bot = telebot.TeleBot(token)

# logging
logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
logging.info("Bot start")
msg = bot.send_message(ADMIN_ID, "Bot start")

# ответ на комманду start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, f'Добрый день {message.chat.first_name}. Я бот для выдачи рандомных анекдотов категории Б \nДля получения анекдота введи /anek')

# ответ на help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(
        message, "Для получения анекдота введи /anek")

# ответ на ping
@bot.message_handler(commands=['p'])
def send_help(message):
    bot.reply_to(message, "Сап!")
    logging.info("ping ok   PID - " + str(os.getpid()))

# обработка не правильного контента
@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def get_non_text(message):
    logging.info(str(message.chat.username) + ": wrong content")
    bot.send_message(message.chat.id,
                     "Чел я не понимаю, введи /anek")
                    
def gen_anek() -> str:
    a = requests.get("https://baneks.site/random")
    anek = re.findall(r'<section itemprop=\"description\"><p>(.*?)</p>', str(a.text))
    return(str(anek[0]).replace('<br/>','\n'))


@bot.message_handler(commands=['anek'])
def bot_search(message):
    bot.send_message(message.chat.id,gen_anek())
    logging.info(f'{message.chat.username} get anek')

try:
    bot.polling(none_stop=True, timeout=4)
except Exception as e:
    logging.error(str(e))
