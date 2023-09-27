import telebot
import webbrowser
from telebot import types
from django.conf import settings
from models import TG_USER


# Вставляем токен бота 
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # # make button 
    # markup = types.ReplyKeyboardMarkup()
    # btn1 = types.KeyboardButton('Our site')
    # btn2 = types.KeyboardButton('Delete photo')
    # markup.row(btn1, btn2)
    # markup.add(types.KeyboardButton('edit photo'))

    if TG_USER.objects.get(user_id, False):
        TG_USER.objects.create(user_id, username, first_name, last_name)
        bot.send_message(message.chat.id, f"Привет, {first_name}! Вы были успешно зарегистрированы.")
    else:
        bot.reply_to(message, f"Мы всегда с вами! {first_name}")
    
    # bot.register_next_step_handler(message, on_click)

# Рассылка всем пользователям
@bot.message_handler(commands=['send_message'])
def send_message(message):
    if message.chat.id == settings.ADMIN_ID:
        users = TG_USER.objects.all()
        text = message.text.replace('/send_message', '').strip()

        for user in users:
            try:
                bot.send_message(user.user_id, text=text)
            except Exception as e:
                print(f'Произошла ошибка {e}')
    else:
        bot.send_message(message.chat.id, 'Вы не администратор')

# def on_click(message):
#     if message.text == 'Our site':
#         bot.send_message(message.chat.id, 'Website is open')

@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://red-store.site')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>Help</b> information', parse_mode='html')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Our site', url='https://red-store.site')
    btn2 = types.InlineKeyboardButton('Delete photo', callback_data='delete')

    markup.row(btn1, btn2)
    markup.add(types.InlineKeyboardButton('edit photo', callback_data='edit'))
    
    bot.reply_to(message, 'Какое красивое фото', reply_markup=markup)

# Выполнение запросов 
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)

    elif callback.data == 'edit':
        bot.edit_message_text('Edit text ', callback.message.chat.id, callback.message.message_id)

# Ловит любое сообщение
@bot.message_handler()
def info(message):
    if message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


# Установка вебхука
bot.remove_webhook()
bot.set_webhook(url=f'https://red-store.site/bot_token/')



