import telebot
from telebot import types
import random
from quiz_functions import get_indexes, get_category_id, get_quiz_menu, start_quiz, send_main_menu, send_test_menu, finish_bot, next_question, get_correct, get_answer, \
    get_count_questions, words1, words2, check_user, get_results
from text_speech import speech_to_text, text_to_speech, verify_word, get_user_response, speech
import random
from teaching import get_menu, get_words_by_category, get_picture_study
from tabulate import tabulate
from ai_talk import get_random_response, get_intent_ml


bot = telebot.TeleBot("6292455306:AAHgBcHGVwIOFIz1bPsNH-aG3EGY6YXdceA")
ind = 0
stat = 0
points = 0
count = 0
propuski = 0
quizzzz = 0
words_shown = False
gaps = 0
answer_choice = 0
pronunciation = 0





@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Study🧠')
    item2 = types.KeyboardButton('Test📝')
    item3 = types.KeyboardButton('Communication🗣')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}', reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    send_main_menu(message)


@bot.message_handler(commands=['rating'])
def menu(message):
    get_results(message, gaps, answer_choice, pronunciation)


class Quiz:
    def __init__(self, path="data.txt"):
        with open(path, "r", encoding='utf-8') as file:
            lines = file.readlines()
            self.questions = [line.strip().split('|') for line in lines]

    def get_next_question(self):
        index = random.randint(0, len(self.questions) - 1)
        question = self.questions[index]
        del self.questions[index]
        return question

class QuestionState:
    def __init__(self):
        self.current_item = None
        self.opened = 0

    @property
    def answer_hint(self):
        return self.current_item[1][:self.opened].ljust(len(self.current_item[1]), '_')

    @property
    def display_question(self):
        return f"{self.current_item[0]} : {len(self.current_item[1])} letters\n{self.answer_hint}"

    @property
    def is_end(self):
        return self.opened == len(self.current_item[1])/2


class GameState:
    def __init__(self):
        self.in_progress = False


quiz = Quiz()
game_state = GameState()
states = {}
user_scores = {}

@bot.message_handler(func=lambda message: message.text == 'Gaps')
def quiz_start(message):
    game_state.in_progress = True
    chat_id = message.chat.id
    if chat_id not in states:
        states[chat_id] = QuestionState()
    state = states[chat_id]
    state.current_item = quiz.get_next_question()
    state.opened = 0
    bot.send_message(chat_id=chat_id, text=state.display_question)



@bot.message_handler(func=lambda message: game_state.in_progress == True and message.text != 'Study🧠' and message.text != 'Communication🗣' and message.text != 'Finalize the bot' and message.text != 'Test📝' and message.text != 'Answer choice')
def quiz_handler(message):
    chat_id = message.chat.id
    if chat_id not in states:
        states[chat_id] = QuestionState()
    state = states[chat_id]
    if state.current_item is None:
        state.current_item = quiz.get_next_question()
    question = state.current_item
    try_answer = message.text.lower()
    if try_answer == question[1].lower():
        from_id = message.from_user.id
        if from_id in user_scores:
            user_scores[from_id] += 1
        else:
            user_scores[from_id] = 1
        bot.send_message(chat_id=chat_id, text=f"That's right!\nYou have {user_scores[from_id]} points")
        gaps = user_scores[from_id]
        new_round(chat_id, message)
    else:
        state.opened += 1
        if state.is_end:
            bot.send_message(chat_id=chat_id, text=f"You didn't get it! It was - {question[1]}")
            new_round(chat_id, message)
        bot.send_message(chat_id=chat_id, text=state.display_question)

def new_round(chat_id, message):
    global count
    count += 1
    if (count < 9):
        if chat_id in states:
            state = states[chat_id]
            state.current_item = quiz.get_next_question()
            if state.current_item:
                state.opened = 0
                bot.send_message(chat_id=chat_id, text=state.display_question)
    else:
        game_state.in_progress = False
        bot.send_message(chat_id=chat_id, text="Quiz completed. Back to the main menu.")
        send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == 'Answer choice')
def send_words(message):
    global answer_choice
    global stat  # уберите эту глобальную переменную, если не используется
    menu_list = get_quiz_menu()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in menu_list:
        markup.add(types.KeyboardButton(item))
    bot.send_message(message.chat.id, 'Select a category:', reply_markup=markup)
    bot.register_next_step_handler(message, handle_category)  # Начинаем с обработки выбора категории


def handle_category(message):
    if message.chat.type == 'private' and message.text in get_quiz_menu():
        global points, ind  # необходимо ли вам использовать globla?
        points = 0  # Сбрасываем счетчик правильных ответов при начале новой категории
        ind = 0  # Сбрасываем индекс вопроса при начале новой категории
        next_question(message, get_indexes(message.text)[ind], points)  # Показываем первый вопрос
        bot.register_next_step_handler(message, lambda msg: handle_answer(msg, message.text))  # Устанавливаем обработчик для ответов


def handle_answer(message, categ):
    global answer_choice
    if message.chat.type == 'private':
        global points, ind
        correct_answer = get_correct(get_indexes(categ)[ind])  # Получаем правильный ответ

        if message.text == correct_answer:  # Если ответ правильный
            points += 1
            bot.send_message(message.chat.id, f"*✅ {random.choice(words1)}*", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"*❌ {random.choice(words2)}*", parse_mode='Markdown')
            bot.send_message(message.chat.id, f"*🌟 The correct answer*: {correct_answer}", parse_mode='Markdown')

        ind += 1  # Увеличиваем индекс для перехода к следующему вопросу
        if ind < get_count_questions(categ):  # Если есть еще вопросы в категории
            next_question(message, get_indexes(categ)[ind], points) # Показываем следующий вопрос
            bot.register_next_step_handler(message, lambda msg: handle_answer(msg, categ))  # Устанавливаем повторный обработчик для следующего вопроса
        else:
            bot.send_message(message.chat.id, "The category is completed")  # Оповещаем об окончании категории
            answer_choice = points
            bot.send_message(message.chat.id, f"The number of correct answers in this category: {points}")  # Выводим количество правильных ответов

            # Обнуляем счетчик и индекс для следующей категории
            ind = 0
            points = 0
            send_main_menu(message)
            bot.register_next_step_handler(message, handle_category)  # Начинаем с обработки выбора категории




@bot.message_handler(func=lambda message: message.text == 'According to the text')
def send_words(message):
    menu_list = get_menu()
    print(menu_list)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in menu_list:
        markup.add(types.KeyboardButton(item))
    bot.send_message(message.chat.id, 'Select a category:', reply_markup=markup)


    def check_category(message):
        if message.chat.type == 'private' and message.text in menu_list:
            table = get_words_by_category(message.text)
            for group in table:
                table = ''
                for pair in group:
                    pair_str = f'<code><b>{pair[0]}</b></code> - {pair[1]}\n\n'
                    table += pair_str

                bot.send_message(message.chat.id, table, parse_mode='HTML')
            send_main_menu(message)

    bot.register_next_step_handler(message, check_category)


@bot.message_handler(func=lambda message: message.text == 'Finalize the bot')
def save_information(message):
    check_user(message, gaps, answer_choice, pronunciation)

@bot.message_handler(func=lambda message: message.text == 'Pronunciation')
def send_words(message):
    menu_list = get_menu()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in menu_list:
        markup.add(types.KeyboardButton(item))
    bot.send_message(message.chat.id, 'Select a category:', reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: check_category(msg, 0))


def check_category(message, index):
    global pronunciation
    menu_list = get_menu()
    if message.chat.type == 'private' and message.text in menu_list:
        pair_groups = get_words_by_category(message.text)[index]
        if index < len(pair_groups):
            word, translation = pair_groups[index]
            audio_check = bot.send_voice(message.chat.id, text_to_speech(word))
            if audio_check is not None:
                bot.register_next_step_handler(message, lambda msg, idx=index: handle_user_response(msg, word, pair_groups, idx + 1))
        else:
            send_main_menu(message)
            bot.send_message(message.chat.id, "All words from this category have been pronounced.")


def handle_user_response(message, word, pair_groups, index):
    global pronunciation
    if message.text:
        user_response = message.text
        verify_word(message, word, user_response, pronunciation)

        if index < len(pair_groups):
            word, translation = pair_groups[index]
            audio_check = bot.send_voice(message.chat.id, text_to_speech(word))
            if audio_check is not None:
                bot.register_next_step_handler(message, lambda msg, idx=index: handle_user_response(msg, word, pair_groups, idx + 1))
        else:
            send_main_menu(message)
            bot.send_message(message.chat.id, "All words from this category have been pronounced.")
    elif message.voice:
        user_response = speech(message)
        print(user_response)
        verify_word(message, word, user_response)

        if index < len(pair_groups):
            word, translation = pair_groups[index]
            audio_check = bot.send_voice(message.chat.id, text_to_speech(word))
            if audio_check is not None:
                bot.register_next_step_handler(message, lambda msg, idx=index: handle_user_response(msg, word, pair_groups, idx + 1))
        else:
            send_main_menu(message)
            print(verify_word(message, word, user_response, pronunciation))
            pronunciation = verify_word(message, word, user_response, pronunciation)
            bot.send_message(message.chat.id, "All words from this category have been pronounced.")


@bot.message_handler(func=lambda message: message.text == 'Communication🗣')
def send_dialog(message):
    if (message.text == 'Goodbye' or message.text == 'Bye' or message.text == 'Stop talk'):
        bot.send_message(message.chat.id, 'Goodbye! See you later')

    else:
        user_text = message.text
        intent = get_intent_ml(user_text)
        if intent:
            reply = get_random_response(intent)
        else:
            intent = get_intent_ml(user_text)
            reply = get_random_response(intent)
        bot.send_message(message.chat.id, reply)
        bot.register_next_step_handler(message, lambda msg: send_dialog(msg))



# Обработчик нажатий кнопок
@bot.message_handler(func=lambda message: True)
def handle_general_messages(message):
    if message.chat.type == 'private':
        if message.text == 'Test📝':  # Проверяем выбранную команду
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            it1 = types.KeyboardButton('Gaps')
            it2 = types.KeyboardButton('Answer choice')
            it3 = types.KeyboardButton('Pronunciation')
            markup.add(it1, it2, it3)
            bot.send_message(message.chat.id, 'Select an action:', reply_markup=markup)
        elif message.text == 'Gaps':
            propuski = 1
            game_state.in_progress = True
        elif message.text == 'Answer choice':
            quizzzz=1
            start_quiz(message)  # Если выбрано "Test📝", запускаем викторину
        elif message.text == 'Study🧠':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('According to the text')
            item2 = types.KeyboardButton('From pictures')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Select an action:', reply_markup=markup)
        elif message.text == 'According to the text':
            menu_list = get_menu()
            print(menu_list)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for item in menu_list:
                markup.add(types.KeyboardButton(item))
            bot.send_message(message.chat.id, 'Select a category:', reply_markup=markup)
        elif message.text == 'Pronunciation':
            menu_list = get_menu()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for item in menu_list:
                markup.add(types.KeyboardButton(item))
            bot.send_message(message.chat.id, 'Select a category:', reply_markup=markup)
        elif message.text == 'From pictures':
            get_picture_study(message)
            send_main_menu(message)
        elif message.text == 'Communication🗣':
            bot.send_message(message.chat.id, 'Общаемся...')
        elif message.text == 'Finalize the bot':
            check_user(message, gaps, answer_choice, pronunciation)
            finish_bot()
        else:
            bot.send_message(message.chat.id, 'Select a menu item to continue.')


bot.polling()