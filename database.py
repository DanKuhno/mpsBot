import psycopg2
import constants
import datetime

def get_connection():
    return psycopg2.connect(constants.dbToken)

def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

def writeNewUser(first_name, last_name, id_user, username ):
    execute_query("INSERT INTO users (first_name, last_name, id_telegram, username) VALUES (%s, %s, %s, %s)",
        (first_name, last_name, id_user, username))


def newAttempt(id_tg):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_users FROM users  WHERE id_telegram = %s",
                (id_tg,))
    id_user = cur.fetchone()[0]

    cur.execute("INSERT INTO attempt (id_users, status) VALUES (%s, %s)",
                (id_user, False))
    conn.commit()
    cur.close()
    conn.close()


def writeMessage(id_tg, id_previous_writing, text_writing_bot, text_writing_user, asked):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_users FROM users  WHERE id_telegram = %s",
                (id_tg,))
    id_user = cur.fetchone()[0]

    cur.execute("SELECT id_attempt FROM attempt  WHERE id_users = %s AND status = false",
                (id_user,))
    id_attempt = cur.fetchone()[0]

    date = datetime.datetime.now()
    cur.execute("INSERT INTO writing (id_attempt, id_previous_writing, text_writing_bot, text_writing_user, asked, datetime) VALUES (%s, %s, %s, %s, %s, %s)",
                (id_attempt, id_previous_writing, text_writing_bot, text_writing_user, asked, date))
    conn.commit()

    cur.execute("SELECT id_writing FROM writing  WHERE id_attempt = %s",
                (id_attempt,))
    id_writing = cur.fetchall()[-1][0]

    cur.close()
    conn.close()
    return id_writing


def updateAskedMessage(id_tg, text_writing_bot):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_users FROM users  WHERE id_telegram = %s",
                (id_tg,))
    id_user = cur.fetchone()[0]

    cur.execute("SELECT id_attempt FROM attempt  WHERE id_users = %s AND status = FALSE",
                (id_user,))
    id_attempt = cur.fetchone()[0]

    date = datetime.datetime.now()

    cur.execute("UPDATE writing SET asked = TRUE, datetime = (%s) WHERE asked = FALSE AND text_writing_bot = (%s) AND id_attempt = (%s)",
                (date, text_writing_bot, id_attempt))
    conn.commit()
    cur.close()
    conn.close()


def updateAnswerMessage (id_tg, text_writing_user):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_users FROM users  WHERE id_telegram = %s",
                (id_tg,))
    id_user = cur.fetchone()[0]

    cur.execute("SELECT id_attempt FROM attempt  WHERE id_users = %s AND status = FALSE",
                (id_user,))
    id_attempt = cur.fetchone()[0]

    cur.execute("UPDATE writing SET text_writing_user = (%s) WHERE asked = TRUE AND text_writing_user IS NULL AND id_attempt=(%s)",
                (text_writing_user, id_attempt))
    conn.commit()
    cur.close()
    conn.close()


def finishAttempt(id_tg):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_users FROM users  WHERE id_telegram = %s",
                (id_tg,))

    id_user = cur.fetchone()[0]

    cur.execute( "UPDATE attempt SET status = true WHERE id_users = (%s)",
        (id_user,))
    conn.commit()
    cur.close()
    conn.close()

def selectQuestion(id_tg):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_users FROM users  WHERE id_telegram = %s",
                (id_tg,))

    id_user = cur.fetchone()[0]

    cur.execute("SELECT id_attempt FROM attempt  WHERE id_users = %s AND status = FALSE",
                (id_user,))
    id_attempt = cur.fetchone()[0]

    cur.execute("SELECT id_writing, text_writing_bot FROM writing WHERE (id_attempt = (%s) AND asked=FALSE)",
                (id_attempt,))
    questions = cur.fetchall()
    print (questions)
    conn.commit()
    cur.close()
    conn.close()
    if len(questions)>0:
        return questions[-1]
    else:
        return

def findIdPrevious(id_tg):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_users FROM users  WHERE id_telegram = %s",
                (id_tg,))
    id_user = cur.fetchone()[0]

    cur.execute("SELECT id_attempt FROM attempt  WHERE id_users = %s AND status = FALSE",
                (id_user,))
    id_attempt = cur.fetchone()[0]


    cur.execute("SELECT id_writing FROM writing WHERE id_attempt = (%s) AND asked = TRUE",
                (id_attempt,))
    idWritings = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    #print(idWritings[-1][0])
    return idWritings[-1][0]

def getAge(id_tg):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT age FROM users  WHERE id_telegram = %s",
                (id_tg,))
    age = cur.fetchone()[0]
    return age

def getGender(id_tg):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT gender FROM users  WHERE id_telegram = %s",
                (id_tg,))
    gender = cur.fetchone()[0]
    return gender

def setAge(id_tg, age):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET age = (%s) WHERE id_telegram = (%s) ",
        (age, id_tg))
    conn.commit()
    cur.close()
    conn.close()

def setGender(id_tg, gender):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET gender = (%s) WHERE id_telegram = (%s) ",
        (gender, id_tg))
    conn.commit()
    cur.close()
    conn.close()