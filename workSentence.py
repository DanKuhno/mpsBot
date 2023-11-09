import random
import phrases
# Функция проверки ответа на стоп-слова
def checkStop(response):
    response = response.strip()
    response = response.lower()
    if response in phrases.stopSentence:
        return True
    return  False


# Функция проверки ответа на содержание фразы "Потому что"
def checkSentence (response):
    response = response.strip()
    response = response.lower()
    if "потому что" in response:
        return True
    return  False

# Создание
def createQuestion(response):
    randPartList = ['А для чего нужно ', 'А зачем нужно ', 'Как ты думаешь, для чего нужно ', 'Как ты думаешь, зачем ']
    randPart = randPartList[random.randint(0, len(randPartList) - 1)]
    questions = []
    for i in response:
        i = i.strip()
        if len(i)>0:
            i = i.lower()
            i = i.replace("чтобы", '')
            question = randPart + i + "?"
            questions.append(question)
    return questions
