import pymysql
import telebot
from telebot import types
from config import host, user, password, db_name
import datetime


connection = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)
bot = telebot.TeleBot("6292455306:AAHgBcHGVwIOFIz1bPsNH-aG3EGY6YXdceA")

words1 = ["The answer is right!", "Way to go!", "Keep up the good work!", "Well done!", "You're doing a good job!"]
words2 = ["Wrong answer!", "Unfortunately you got it wrong", "You failed", "You failed this time", "Pay more attention"]

cursor = connection.cursor()

def get_quiz_menu():
    cursor.execute("SELECT category_name FROM categories_for_test")
    menu_items = cursor.fetchall()
    category_names = [item['category_name'] for item in menu_items]
    return category_names

def get_category_id(category):
    cursor.execute(f"SELECT category_id FROM categories_for_test WHERE category_name = '{category}'")
    query_result = cursor.fetchall()
    for res in query_result:
        return res['category_id']



def get_question(name):
    questions = []
    question = f"SELECT text FROM questions WHERE category_code = {get_category_id(name)}"
    cursor.execute(question)
    query_result = cursor.fetchall()
    for res in query_result:
        questions.append(res['text'])
    return questions

def get_indexes(name):
    indexes = []
    question = f"SELECT question_code FROM questions WHERE category_code = {get_category_id(name)}"
    cursor.execute(question)
    query_result = cursor.fetchall()
    for res in query_result:
        indexes.append(res['question_code'])
    return indexes

def get_count_questions(name):
    size = len(get_question(name))
    return size


def get_answer(index, variant):
    query = f"SELECT {variant} FROM answers WHERE question_code = {index}"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
        return result[variant]


def get_correct(index):
    with connection.cursor() as cursor:
        query = f"SELECT correct FROM questions WHERE question_code = {index}"
        cursor.execute(query)
        query_result = cursor.fetchall()
        for res in query_result:
            return res['correct']

def get_question_index(index):
    question = f"SELECT text FROM questions WHERE question_code = {index}"
    cursor.execute(question)
    query_result = cursor.fetchall()
    for res in query_result:
        return res['text']


def get_pictures(index):
    question = f"SELECT picture FROM questions WHERE question_code = {index}"
    cursor.execute(question)
    query_result = cursor.fetchall()
    for res in query_result:
        return res['picture']


def get_audio(index):
    question = f"SELECT audio FROM questions WHERE question_code = {index}"
    cursor.execute(question)
    query_result = cursor.fetchall()
    for res in query_result:
        return res['audio']


def next_question(message, index, points):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [get_answer(index, 'a'), get_answer(index, 'b'), get_answer(index, 'c'), get_answer(index, 'd')]
    for button_text in buttons:
        button = types.KeyboardButton(button_text)
        markup.row(button)
    if (get_pictures(index) == None and get_audio(index) == None):
        bot.send_message(message.chat.id, f'❔_{get_question_index(index)}_❔', reply_markup=markup, parse_mode='Markdown')
    elif get_pictures(index) != None:
        file = open(f'images/test/{get_pictures(index)}', 'rb')
        bot.send_message(message.chat.id, f'❔_{get_question_index(index)}_❔', reply_markup=markup, parse_mode='Markdown')
        bot.send_photo(message.chat.id, file, reply_markup=markup)
    else:
        file = open(f'audio/{get_audio(index)}', 'rb')
        bot.send_message(message.chat.id, f'❔_{get_question_index(index)}_❔', reply_markup=markup, parse_mode='Markdown')
        bot.send_audio(message.chat.id, file, reply_markup=markup)


def start_quiz(message):
    global index, points
    index = 1
    points = 0
    next_question(message, index, points)  # Начать викторину, проигрывая первый вопрос


def send_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Study🧠')
    item2 = types.KeyboardButton('Test📝')
    item3 = types.KeyboardButton('Communication🗣')
    item4 = types.KeyboardButton('Finalize the bot')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Select an action:', reply_markup=markup)


def send_test_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    it1 = types.KeyboardButton('Gaps')
    it2 = types.KeyboardButton('Answer choice')
    it3 = types.KeyboardButton('Pronunciation')
    markup.add(it1, it2, it3)
    bot.send_message(message.chat.id, 'Select an action:', reply_markup=markup)


def finish_bot():
    bot.stop_polling()
    exit()


def check_user(message, gaps, answer_choice, pronunciation):
    cursor.execute(f"SELECT user_code FROM users WHERE telegram_code = '{message.chat.id}'")
    n = 0
    result = cursor.fetchall()
    if result:
        for res in result:
            print(res['user_code'])
            n = res['user_code']
    else:
        cursor.execute(f"INSERT INTO users (telegram_code) VALUES ('{message.chat.id}')")
        connection.commit()  # Фиксация изменений

        cursor.execute(f"SELECT user_code FROM users WHERE telegram_code = '{message.chat.id}'")
        result = cursor.fetchall()
        for res in result:
            n = res['user_code']
     # Получить текущую дату и время
    now = datetime.datetime.now()
    # Преобразовать дату и время в нужный формат
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO tests (user_code, gaps, answer_choice, pronunciation, date) VALUES (%s, %s, %s, %s, %s)",
        (n, gaps, answer_choice, pronunciation, formatted_datetime))
    connection.commit()



def get_results(message, gaps, answer_choice, pronunciation):
    question = f"SELECT user_code FROM users WHERE telegram_code = {message.chat.id}"
    cursor.execute(question)
    query_result = cursor.fetchall()
    for res in query_result:
        print(res['user_code'])
        if res['user_code']:
            ques = f"SELECT MAX(gaps) AS max_gaps, MAX(answer_choice) AS max_answer_choice, MAX(pronunciation) AS max_pronunciation FROM tests WHERE user_code = {res['user_code']}"
            cursor.execute(ques)
            result = cursor.fetchone()
            print(result)
            # Соединяем значения в одну строку
            res = f"Максимальный результат gaps: {result['max_gaps']}.\nМаксимальный результат answer_choice: {result['max_answer_choice']}.\nМаксимальный результат pronunciation: {result['max_pronunciation']}"
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Вы ещё не проходили задания")




