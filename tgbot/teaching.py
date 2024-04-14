import pymysql
import telebot
from telebot import types
from config import host, user, password, db_name
from tabulate import tabulate
import prettytable as pt
from prettytable import PrettyTable



connection = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)

bot = telebot.TeleBot("6292455306:AAHgBcHGVwIOFIz1bPsNH-aG3EGY6YXdceA")

cursor = connection.cursor()

def send_teach_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('According to the text')
    item2 = types.KeyboardButton('From pictures')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


def get_menu():
    cursor.execute("SELECT category_name FROM categories_of_words")
    menu_items = cursor.fetchall()
    category_names = [item['category_name'] for item in menu_items]
    return category_names


def get_words(category_name):
    cursor.execute(f"SELECT category_code FROM categories_of_words WHERE category_name = '{category_name}'")
    word_data = cursor.fetchall()
    for res in word_data:
        return res['category_code']

def get_picture_study(message):
    cursor.execute(f"SELECT picture_path, text, text_in_english FROM study_with_pictures")
    word_data = cursor.fetchall()
    for image in word_data:
        data = []
        image_path = image['picture_path']  # Путь к изображению
        image_text = image['text']  # Текст картинки
        translate = image['text_in_english']
        file = open(f'images/training/{image_path}', 'rb')
        bot.send_photo(message.chat.id, file)
        data.append([image_text, translate])
        table = tabulate(data, headers=["Word", "Translate"], tablefmt="pretty", colalign=("left", "left"))
        bot.send_message(message.chat.id, f'<pre>{table}</pre>', parse_mode='HTML')


def get_words_by_category(category):
    code = get_words(category)
    cursor.execute(f"SELECT word, translation FROM study_words_in_text WHERE category = {code}")
    word_data = cursor.fetchall()
    words = []
    translations = []
    word_translation_pairs = []
    for res in word_data:
        word = res['word']
        words.append(word)
        translation = res['translation']
        translations.append(translation)
        word_translation_pairs.append([word, translation])
        chunk_size = 10  # Максимальное количество слов в каждой таблице
        pair_groups = [word_translation_pairs[i:i + chunk_size] for i in range(0, len(word_translation_pairs), chunk_size)]
    return pair_groups










