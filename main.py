import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
user_data = {}


# class User_register:
#    def __init__(self, login):
#        self.login = login
#        self.password = " "
#        self.email = " "
#        self.category = " "


@bot.message_handler(commands=['about'])
def txt(message):
    bot.send_message(message.chat.id, 'Здравствуйте, это телеграм бот для знакомств. \nНаша главная цель - '
                                      'найти то, что вам нужно будь то общение или отношения.\nСоветуем '
                                      'пройти регистрацию, чтоб скоее сделать это!', parse_mode="HTML")


@bot.message_handler(commands=['connection'])
def connection(message):
    bot.send_message(message.chat.id, 'Если что-то не так обращайтесь к разработчикам @Raa_is @daniil170301')


@bot.message_handler(commands=['start'])
def hello(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    reg = types.KeyboardButton('Регистрация')
    markup.add(reg)
    msg = bot.send_message(message.chat.id, 'Здравствуйте, это телеграм бот для знакомств. \nНаша главная цель - '
                                            'найти то, что вам нужно будь то общение или отношения.\nСоветуем '
                                            'пройти регистрацию, чтоб скоее сделать это!', parse_mode="HTML",
                           reply_markup=markup)

    bot.register_next_step_handler(msg, send_name)


def send_name(message):
    if message.text.lower() == 'регистрация':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        name = types.KeyboardButton("{0.first_name}".format(message.from_user))
        markup.add(name)
        msg = bot.send_message(message.chat.id, "Как вас зовут? ", reply_markup=markup)
        bot.register_next_step_handler(msg, send_age)
    else:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.from_user.id, 'Просим прощения за беспокойство, приходите ещё)', reply_markup=markup)


def send_age(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Сколько Вам лет? \n <i>Просим указывать честный возраст</i>",
                           parse_mode="html", reply_markup=markup)
    bot.register_next_step_handler(msg, send_city)


def send_city(message):
    try:
        if 12 > int(message.text) or int(message.text) > 100:
            bot.send_message(message.from_user.id, "Вам нужно ввести возраст от 12 и до 100!")
            send_age(message)
            return
    except ValueError:
        bot.send_message(message.from_user.id, "Вам нужно ввести возраст!")
        send_age(message)
        return
    try:
        # /////////
        msg = bot.send_message(message.chat.id, "Введите город? ")
        bot.register_next_step_handler(msg, send_gender)
    except Exception as e:
        bot.reply_to(message, f'oops!! {e}')


def send_gender(message):
    if message.content_type == 'location':
        print(message.location)
    elif message.content_type == 'text':
        print(message.text)
    else:
        print('//тут надо обратно отправить')
    # /////////
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    men = types.KeyboardButton('Я парень')
    fem = types.KeyboardButton('Я девушка')
    xz = types.KeyboardButton('Я вертолет')
    markup.add(men, fem, xz)
    msg = bot.send_message(message.from_user.id, "Давайте определим Ваш пол: ", reply_markup=markup)
    bot.register_next_step_handler(msg, send_target)


def send_target(message):
    if (message.text != 'Я парень') and (message.text != 'Я девушка') and (message.text != 'Я вертолет'):
        bot.send_message(message.from_user.id, 'Нужно ввести что-то из предложенного')
        send_gender(message)
        return
    # ///////////////
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    communication = types.KeyboardButton('Общение')
    couple = types.KeyboardButton('Найти пару')
    sex = types.KeyboardButton('Быстрые знакомства')
    markup.add(communication, couple, sex)

    msg = bot.send_message(message.from_user.id, 'Выберите свои цели:', reply_markup=markup)
    bot.register_next_step_handler(msg, send_search_target)


def send_search_target(message):
    if (message.text != 'Общение') and (message.text != 'Найти пару') and (message.text != 'Быстрые знакомства'):
        bot.send_message(message.from_user.id, 'Нужно ввести что-то из предложенного')
        send_target(message)
        return
    # Запиши данные
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    men = types.KeyboardButton('Парни')
    women = types.KeyboardButton('Девушки')
    helicopter = types.KeyboardButton('Вертолеты')
    all = types.KeyboardButton('Всё равно')
    markup.add(men, women, helicopter, all)

    msg = bot.send_message(message.from_user.id, 'Кто тебе интересен?', reply_markup=markup)
    bot.register_next_step_handler(msg, send_photo)


def send_photo(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.from_user.id, 'Отправьте своё фото \n <i>Пожалуйста отправляйте свою фотографию</i>',
                           parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(msg, last_process)


def last_process(message):
    if message.content_type == 'photo':
        print(message.photo[2].file_id)#'AgACAgIAAxkBAAIJkWCillIiAs6x979Y04dnM6IkdnvRAALKsjEbTK8ZSfB_Vo5xTtSJPqlapC4AAwEAAwIAA3gAA8YgAQABHwQ'
        print(message.photo[2].file_unique_id)
        #сохранить #'AQADPqlapC4AA8YgAQAB'
    else:
        send_photo(message)
        return
    # Тут надо записывать данные
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Окей \n Вы успешно зарегистрированы.", reply_markup=markup)
    print('Регистрация')


bot.polling()
