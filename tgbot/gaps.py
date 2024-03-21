import random

import telebot as telebot
from telegram import Update
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

bot = telebot.TeleBot("6292455306:AAHgBcHGVwIOFIz1bPsNH-aG3EGY6YXdceA")


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
        return f"{self.current_item[0]} : {len(self.current_item[1])} букв\n{self.answer_hint}"

    @property
    def is_end(self):
        return self.opened == len(self.current_item[1])

quiz = Quiz()
updater = Updater(token="6292455306:AAHgBcHGVwIOFIz1bPsNH-aG3EGY6YXdceA", use_context=True)
dispatcher = updater.dispatcher

states = {}
user_scores = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот с викторинами. Напиши "/quiz" для начала игры.')

def quiz_start(update, context):
    chat_id = update.message.chat_id
    if chat_id not in states:
        states[chat_id] = QuestionState()
    state = states[chat_id]
    state.current_item = quiz.get_next_question()
    state.opened = 0
    context.bot.send_message(chat_id=chat_id, text=state.display_question)

quiz_start_handler = CommandHandler('quiz', quiz_start)
dispatcher.add_handler(quiz_start_handler)

def quiz_handler(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in states:
        states[chat_id] = QuestionState()
    state = states[chat_id]
    if state.current_item is None:
        state.current_item = quiz.get_next_question()
    question = state.current_item
    try_answer = update.message.text.lower().replace('ё', 'е')
    if try_answer == question[1]:
        from_id = update.message.from_user.id
        if from_id in user_scores:
            user_scores[from_id] += 1
        else:
            user_scores[from_id] = 1
        context.bot.send_message(chat_id=chat_id, text=f"Правильно!\nУ вас {user_scores[from_id]} очков")
        new_round(chat_id)
    else:
        state.opened += 1
        if state.is_end:
            context.bot.send_message(chat_id=chat_id, text=f"Никто не отгадал! Это было - {question[1]}")
            new_round(chat_id)
        context.bot.send_message(chat_id=chat_id, text=state.display_question)

def new_round(chat_id):
    if chat_id not in states:
        states[chat_id] = QuestionState()
    state = states[chat_id]
    state.current_item = quiz.get_next_question()
    state.opened = 0
    bot.send_message(chat_id=chat_id, text=state.display_question)



start_handler = CommandHandler('start', start)
quiz_handler = MessageHandler(Filters.text & (~Filters.command), quiz_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(quiz_handler)

updater.start_polling()
