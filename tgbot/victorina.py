import telebot
import pymysql
from telebot import types
import random
import time
from config import host, user, password, db_name

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        cursor = connection.cursor()
        def get_question(index):
            question = f"SELECT text FROM questions WHERE id = {index}"
            cursor.execute(question)
            query_result = cursor.fetchall()
            for res in query_result:
                return res['text']


        def get_answer(index, variant):
            query = f"SELECT {variant} FROM answers WHERE question_code = {index}"
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result[variant]


        def get_correct(index):
            with connection.cursor() as cursor:
                query = f"SELECT correct FROM questions WHERE questions.id = {index}"
                cursor.execute(query)
                query_result = cursor.fetchall()
                for res in query_result:
                    return res['correct']

        def next_question(message, index, points):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(get_answer(index, 'a')),
                       types.KeyboardButton(get_answer(index, 'b')),
                       types.KeyboardButton(get_answer(index, 'c')),
                       types.KeyboardButton(get_answer(index, 'd')))
            bot.send_message(message.chat.id, f'{get_question(index)}', reply_markup=markup)



        bot = telebot.TeleBot("6292455306:AAHgBcHGVwIOFIz1bPsNH-aG3EGY6YXdceA")
        index = 1
        points = 0

        words1 = ["Ответ правильный!", "Так держать!", "Продолжай в том же духе", "Молодец!", "У тебя хорошо получается"]
        random1 = random.choice(words1)

        words2 = ["Ответ НЕправильный!", "К сожалению у тебя неправильно", "У тебя не получилось", "На этот раз у тебя не вышло", "Будь вниматильнее"]
        random1_ = random.choice(words2)


        def start_quiz(message):
            global index, points
            index = 1
            points = 0
            next_question(message, index, points)  # Начать викторину, проигрывая первый вопрос


        # Функция для вывода следующего вопроса
        def next_question(message, index, points):
            question = get_question(index)  # Получаем текст вопроса из базы данных
            buttons = [get_answer(index, 'a'), get_answer(index, 'b'), get_answer(index, 'c'), get_answer(index, 'd')] # Получаем варианты ответов на вопрос из базы данных
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for button_text in buttons:
                markup.add(types.KeyboardButton(button_text))
            bot.send_message(message.chat.id, question, reply_markup=markup)

            # Функция для вывода главного меню

        def send_main_menu(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Обучение🧠')
            item2 = types.KeyboardButton('Тестирование📝')
            item3 = types.KeyboardButton('Общение🗣')
            item4 = types.KeyboardButton('Завершить работу с ботом')
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)



        @bot.message_handler(func=lambda message:message.text != 'Обучение🧠' and message.text != 'Общение🗣' and message.text != 'Завершить работу с ботом' and message.text != 'Тестирование📝' and message.text != 'Пропуски')
        def handle_answer(message):
            global index, points
            if message.text == 'Выбор ответа':
                next_question(message, index, points)
            if index < 5:
                correct_answer = get_correct(index)
                if message.text == get_answer(index, 'a') or message.text == get_answer(index,'b') or message.text == get_answer(index, 'c') or message.text == get_answer(index, 'd'):
                    if message.text == correct_answer:  # Если ответ правильный
                        points += 1
                        bot.send_message(message.chat.id, random1)
                    else:
                        bot.send_message(message.chat.id, random1_)
                        bot.send_message(message.chat.id, f"Правильный ответ: {correct_answer}")
                    index += 1
                    next_question(message, index, points)
                else:
                    bot.send_message(message.chat.id, "Пожалуйста, выберите ответ из предоставленных вариантов.")
            else:  # Викторина завершена после всех вопросов
                correct_answer = get_correct(index)
                if message.text == correct_answer:  # Если ответ на последний вопрос правильный
                    points += 1
                    bot.send_message(message.chat.id, random1)
                else:
                    bot.send_message(message.chat.id, random1_)
                    bot.send_message(message.chat.id, f"Правильный ответ: {correct_answer}")
                bot.send_message(message.chat.id, "Викторина окончена")
                bot.send_message(message.chat.id, f"Количество правильных ответов: {points}")
                # Сбросить индекс и очки для возможности проведения викторины снова
                index = 1
                points = 0
                send_main_menu(message)

    finally:
        connection.close()
        print("successfully connected...")

except Exception as ex:
    print("Connecting refused...")
    print(ex)