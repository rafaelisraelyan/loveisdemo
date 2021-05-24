import telebot
from telebot import types
import config
import psycopg2


class User:
    def __init__(self):
        self.name = ''
        self.gender = ''
        self.age = 0
        self.city = ''
        self.search_gender = ''
        self.photo_id = ''
        self.hobbies = ''
        self.description = ''
        self.target = ''
        self.ms_id = 0
        self.longitude = 0
        self.latitude = 0
        self.file_unique_id = 0
        self.update = False


bot = telebot.TeleBot(config.TOKEN, parse_mode='HTML')
connection_bd = psycopg2.connect(dbname=config.db_name, user=config.db_user, password=config.db_password,
                                 host=config.db_host)
cursor = connection_bd.cursor()
user_data = {}


@bot.message_handler(commands=['about'])
def txt(message):
    bot.send_message(message.chat.id, 'Здравствуйте, это телеграм бот для знакомств. \nНаша главная цель - '
                                      'помочь вам найти здесь общение или отношения.\nСоветуем скорее '
                                      'пройти регистрацию, чтобы сделать это!', parse_mode="HTML")


@bot.message_handler(commands=['connection'])
def connection(message):
    bot.send_message(message.chat.id,
                     'Обнаружили ошибку или хотите что-то предложить? Обращайтесь к разработчикам @Raa_is @El1Tiburon')


@bot.message_handler(commands=['start'])
def hello(message):
    cursor.execute("SELECT * FROM loveis.public.users WHERE ms_id = (%s)", [message.chat.id])

    result = cursor.fetchall()
    print(result)
    if len(result) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        reg = types.KeyboardButton('Регистрация')
        markup.add(reg)
        msg = bot.send_message(message.chat.id, 'Здравствуйте, это телеграмм бот для знакомств. \nНаша главная цель - '
                                                'помочь вам найти здесь общение или отношения.\nСоветуем скорее '
                                                'пройти регистрацию, чтобы сделать это!', parse_mode="HTML",
                               reply_markup=markup)
        if message.chat.username is None:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, 'Вам в настройках телеграмма необдоходимо указать свой @username, '
                                              'а после снова '
                                              'воспользоваться в боте комадой /start', markup)
            return
        bot.register_next_step_handler(msg, send_name)
    else:
        markup1 = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'Вы уже зарегестрирвоались ранее.', reply_markup=markup1)
        markup = types.ReplyKeyboardMarkup(selective=True, row_width=2, resize_keyboard='true')
        yes = types.KeyboardButton('Да')
        no = types.KeyboardButton('Нет')
        # show = types.KeyboardButton('Показать мою анкету') TODO Сделать вывод анкеты
        markup.add(yes, no)
        msq = bot.send_message(message.chat.id, 'Хотите обновить анкету?', reply_markup=markup)
        bot.register_next_step_handler(msq, send_name)


def send_name(message):
    if (message.text.lower() == 'регистрация') or (message.text.lower() == 'да'):
        user_data[message.chat.id] = User()
        if message.text.lower() == 'да':
            user = user_data[message.chat.id]
            user.update = True
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

    user = user_data[message.chat.id]
    user.name = message.text
    bot.register_next_step_handler(msg, send_city)


def send_city(message):
    try:
        if 12 > int(message.text) or int(message.text) > 100:
            bot.send_message(message.from_user.id, "Вам нужно ввести возраст от 12 до 100!")
            send_age(message)
            return
    except ValueError:
        bot.send_message(message.from_user.id, "Вам нужно ввести возраст!")
        send_age(message)
        return
    try:
        # /////////
        user = user_data[message.chat.id]
        user.age = message.text
        msg = bot.send_message(message.chat.id, "Введите город? \n<i>Для точности лучше отправьте геопозиция</i>",
                               parse_mode='html')
        bot.register_next_step_handler(msg, send_gender)
    except Exception as e:
        bot.reply_to(message, f'oops!! {e}')


def send_gender(message):
    if message.content_type == 'location':
        user = user_data[message.chat.id]
        user.longitude = message.location.longitude
        user.latitude = message.location.latitude
    elif message.content_type == 'text':
        user = user_data[message.chat.id]
        user.city = message.text
    else:
        user = user_data[message.chat.id]
        message.text = user.age
        send_city(message)
        return
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
        message.text = ''
        send_gender(message)
        return
    user = user_data[message.chat.id]
    user.gender = message.text
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
        user = user_data[message.chat.id]
        message.text = user.gender
        send_target(message)
        return
    user = user_data[message.chat.id]
    user.target = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    men = types.KeyboardButton('Парни')
    women = types.KeyboardButton('Девушки')
    helicopter = types.KeyboardButton('Вертолеты')
    all = types.KeyboardButton('Всё равно')
    markup.add(men, women, helicopter, all)

    msg = bot.send_message(message.from_user.id, 'Кто тебе интересен?', reply_markup=markup)
    bot.register_next_step_handler(msg, send_photo)


def send_photo(message):
    if (message.text != 'Парни') and (message.text != 'Девушки') and (message.text != 'Вертолеты') and (
            message.text != 'Всё равно'):
        bot.send_message(message.from_user.id, 'Нужно ввести что-то из предложенного')
        user = user_data[message.chat.id]
        message.text = user.target
        send_search_target(message)
        return
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.from_user.id, 'Отправьте своё фото \n <i>Пожалуйста отправляйте свою фотографию</i>',
                           parse_mode='html', reply_markup=markup)
    user = user_data[message.chat.id]
    user.search_gender = message.text
    bot.register_next_step_handler(msg, send_description)


def send_description(message):
    if message.content_type == 'photo':
        print(message.photo[1].file_id)
        print(message.photo[1].file_unique_id)
        user = user_data[message.chat.id]
        user.photo_id = message.photo[1].file_id
        user.file_unique_id = message.photo[1].file_unique_id
    else:
        user = user_data[message.chat.id]
        message.text = user.search_gender
        send_photo(message)
        return
    # TODO сделать так, чтобы если у человека была анкета, то ему предлагали оставить предыдущее !!!Cделал в регистре!!!
    msg = bot.send_message(message.chat.id, "Напишите что-нибудь о себе")
    bot.register_next_step_handler(msg, last_process)


def last_process(message):
    # Тут надо записывать данные
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard='true')
    yes = types.KeyboardButton('Да')
    no = types.KeyboardButton('Нет')
    markup.add(yes, no)
    user = user_data[message.chat.id]
    user.description = message.text
    bot.send_photo(message.chat.id, user.photo_id,
                   caption=f'{user.name} {user.age} - {user.city} \n {user.description}')
    msq = bot.send_message(message.chat.id, 'Всё верно?', reply_markup=markup)
    bot.register_next_step_handler(msq, end_registr)


def end_registr(message):
    user = user_data[message.chat.id]
    cursor.execute("SELECT id FROM users WHERE ms_id = (%s)", [message.chat.id])
    result = cursor.fetchall()
    if message.text.lower() == 'да':
        try:
            if user.update:
                cursor.execute("UPDATE users SET name = %s, gender = %s, age = %s, city = %s,search_gender = %s, "
                               "photo_id = %s, hobbies = %s,target = %s,description = %s, ms_id = %s, latitude = %s, longitude = %s, "
                               "file_unique_id = %s, us_url = %s WHERE id = %s;",
                               (user.name, user.gender, user.age, user.city, user.search_gender, user.photo_id, user.hobbies,
                                user.target, user.description, message.chat.id, user.latitude, user.longitude, user.file_unique_id,
                                message.chat.username, result[0]))
                connection_bd.commit()
            else:
                cursor.execute(
                "INSERT INTO users (NAME,GENDER,age,city,search_gender,photo_id,"
                "hobbies,target,description,ms_id,latitude,longitude,file_unique_id,us_url) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s);",
                (user.name, user.gender, user.age, user.city, user.search_gender, user.photo_id, user.hobbies,
                 user.target, user.description, message.chat.id, user.latitude, user.longitude, user.file_unique_id,
                 message.chat.username))
                connection_bd.commit()
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "Окей \n Вы успешно зарегистрированы.", reply_markup=markup)
            print('Регистрация')
            user_data[message.chat.id] = None
        except Exception:
            bot.send_message(message.chat.id, 'Неизвестная ошибка')
            message.text = 'Регистрация'
            send_name(message)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Попробуйте снова)')
        message.text = 'Регистрация'
        send_name(message)
    else:
        last_process(message)



bot.polling()
