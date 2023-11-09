import telebot
import random
from workSentence import *
import database
import constants
import phrases
import psycopg2
import re

bot = telebot.TeleBot(constants.token)


@bot.message_handler(commands=["start"])
def start(message, res=False):
    id_user = message.from_user.id
    keyAge = False
    try:
        database.writeNewUser(message.from_user.first_name, message.from_user.last_name,
                              id_user, message.from_user.username )
        keyAge = True
    except psycopg2.errors.UniqueViolation:
        print("Пользователь уже есть в БД")

    database.finishAttempt(id_user)
    database.newAttempt(id_user)
    bot.send_message(message.chat.id, phrases.attentionMessage)
    bot.send_message(message.chat.id, phrases.welcomeMessage)

    if keyAge:
        bot.send_message(message.chat.id, phrases.askAge)
        database.writeMessage(id_user, None, phrases.askAge, None, True)
    else:
        currentQuestion = phrases.listQuestions[random.randint(0, len(phrases.listQuestions) - 1)]
        bot.send_message(message.chat.id, currentQuestion)
        database.writeMessage(id_user, None, currentQuestion, None, True)

@bot.message_handler(content_types=["text"])
def handle_text(message):
        global questions
        id_user = message.from_user.id

        database.updateAnswerMessage(id_user, message.text)

        if database.getAge(id_user) is None:
            database.setAge(id_user, 1)
            bot.send_message(message.chat.id, phrases.askGender)
            database.writeMessage(id_user, None, phrases.askGender, None, True)

        elif database.getGender(id_user) is None:
            database.setGender(id_user, True)
            currentQuestion = phrases.listQuestions[random.randint(0, len(phrases.listQuestions) - 1)]
            bot.send_message(message.chat.id, currentQuestion)
            database.writeMessage(id_user, None, currentQuestion, None, True)

        else:

            if not checkStop(message.text):
                s = str(message.text)
                s = re.split(r"[.;]+", s)
                questions = createQuestion(s)
                idPrevious = database.findIdPrevious(id_user)
                for i in questions:
                    idWriting = database.writeMessage(id_user, idPrevious, i, None, False)

            newQuestions = database.selectQuestion(id_user)
            if newQuestions is not None:
                newQuestion = newQuestions[1]
                idQuestion = newQuestions[0]
                bot.send_message(message.chat.id, newQuestion)
                database.updateAskedMessage(id_user, newQuestion)
            else:
                bot.send_message(message.chat.id, phrases.endMessage)
                database.finishAttempt(message.from_user.id)




# Запускаем бота
bot.polling(none_stop=True, interval=0)