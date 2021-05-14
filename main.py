import telebot
from telebot import types

bot = telebot.TeleBot('1725357975:AAElvIeG4NcyCxCXrhfjxHBvPixCne-vPpY')
user_data = {}

class User_register:
    def __init__(self, login):
        self.login = login
        self.password = " "
        self.email = " "
        self.category = " "

@bot.message_handler(commands=['start'])
def send_login(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Как вас зовут? ", reply_markup=markup)
    bot.register_next_step_handler(msg, send_password)


def send_password(message):
    user_id = message.from_user.id
    user_data[user_id] = User_register(message.text)
    msg = bot.send_message(message.chat.id, "Введите пароль: ")
    bot.register_next_step_handler(msg, send_email)


def send_email(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.email = message.text
    msg = bot.send_message(message.chat.id, "Введите email: ")
    bot.register_next_step_handler(msg, send_category)


def send_category(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.category = message.text
    msg = bot.send_message(message.from_user.id, "Введите Вашу группу: ")
    bot.register_next_step_handler(msg, last_process)


def last_process(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.category = message.text
    bot.send_message(message.chat.id, "Вы успешно зарегистрированы.")
    print(user_data)

bot.polling()
