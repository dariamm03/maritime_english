import gtts
import speech_recognition as sr
from pydub import AudioSegment
import string
import telebot


bot = telebot.TeleBot("6292455306:AAHgBcHGVwIOFIz1bPsNH-aG3EGY6YXdceA")


def text_to_speech(msg):
    tts = gtts.gTTS(msg, lang='en')
    tts.save('audio/for_test_speech.mp3')
    file = open(f'audio/for_test_speech.mp3', 'rb')
    return file

def speech(message):
    file = bot.get_file(message.voice.file_id)
    bytes = bot.download_file(file.file_path)
    with open('voice.ogg', 'wb') as f:
        f.write(bytes)
    text = speech_to_text()
    return text

def ogg2wav(ofn):
    wfn = ofn.replace('.ogg', '.wav')
    segment = AudioSegment.from_file(ofn)
    segment.export(wfn, format='wav')

def speech_to_text():
    ogg2wav('voice.ogg')
    r = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
        audio = r.record(source)
        text = r.recognize_google(audio_data=audio)
        return text

def remove_punctuation(word):
    translator = str.maketrans('', '', string.punctuation)
    word_without_punctuation = word.translate(translator).replace(" ", "").strip()
    return word_without_punctuation

def verify_word(message, word, user_response, points):
    if remove_punctuation(word.lower()) == remove_punctuation(user_response.lower()):
        bot.send_message(message.chat.id, "*✅ Молодец! Вы правильно произнесли слово*", parse_mode='Markdown')
        points += 1
    else:
        bot.send_message(message.chat.id, f"*❌ Неправильно. Твоё слово: {user_response.lower()} Правильное слово было:* {remove_punctuation(word.lower())}", parse_mode='Markdown')
    return  points

def get_user_response():
    # Предоставьте пользователю возможность ответить текстом или голосом
    # записать этот ответ, чтобы его можно было сравнить с изначальным словом
    user_response = input("Введите или произнесите слово: ")
    return user_response

def process_user_input(message):
    if message.text:
        text_input = message.text
        return text_input
    elif message.voice:
        # Пользователь отправил аудиосообщение
        # Распознавание голоса здесь может потребовать дополнительной обработки (например, с помощью библиотеки для распознавания голоса)
        audio_input = speech(message)  # Здесь должен быть код распознавания и преобразования аудио в текст
        # Обработка распознанного текста из аудиосообщения
        return audio_input
    else:
        text = "не тот тип"
        return text