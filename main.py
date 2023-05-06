import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from config import TOKEN

question_number = 1
sc = ''

questions = ["Как вы относитесь к ограничению свободы слова и выражения мнений",
             "Как вы относитесь к роли государства в регулировании СМИ и интернета",
             "Как вы относитесь к регулированию государством экономики",
             "Как вы относитесь к обеспечению государством социальной справедливости и поддержке малоимущих граждан",
             "Как вы относитесь к повышению налога на богатство", "Как вы относитесь к религии",
             "Как вы относитесь к социальному равенству", "Как вы относитесь к крупным корпорациям",
             "Как вы относитесь к сохранению национальной идентичности и культурного наследия",
             "Как вы относитесь к свободному ношению оружия",
             "Как вы относитесь к бесплатному здравоохранению",
             "Как вы относитесь к децентрализации государства",
             "Как вы относитесь к профсоюзам"]

answers = []
'''
Хранить всё в глобальном списке - плохая идея 
(надо будет как-то аккуртано обрабатывать ответы нескольких пользователей одновременно)
'''
total_score = []

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

reply_keyboard = [['/start', '/stop'],
                  ['+', '-'],
                  ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

logger = logging.getLogger(__name__)


# Непонятно, зачем context во всех этих функциях
async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def help(update, context):
    await update.message.reply_text("Я в подвале меня заставляют работать я незнаю что делать")


async def start(update, context):
    await update.message.reply_text(
        "Как вы относитесь к ограничению свободы слова и выражения мнений", reply_markup=markup)
    return 1


async def response(update, context):
    global question_number
    global questions
    global answers
    question_number += 1
    await update.message.reply_text(questions[question_number])
    answers.append(update.message.text)
    return question_number


# Очень грустно смотреть на код этой функции - много копипасты(
async def count(update, context):
    # Можно было в одной строке все global перечислить
    global answers
    global total_score

    left_score = 0
    right_score = 0
    liberal_score = 0
    authoritarian_score = 0
    social_score = 0
    economic_score = 0

    if answers[0] == "+":
        authoritarian_score += 1
    else:
        liberal_score += 1

    if answers[1] == "-":
        liberal_score += 1
    else:
        authoritarian_score += 1

    if answers[2] == "+":
        social_score += 1
    else:
        economic_score += 1

    if answers[3] == "-":
        economic_score += 1
    else:
        social_score += 1

    if answers[4] == "+":
        social_score += 1
    else:
        economic_score += 1

    if answers[5] == "-":
        left_score += 1
    else:
        right_score += 1

    if answers[6] == "+":
        left_score += 1
    else:
        right_score += 1

    if answers[7] == "-":
        social_score += 1
    else:
        economic_score += 1

    if answers[8] == "-":
        left_score += 1
    else:
        right_score += 1

    if answers[9] == "-":
        left_score += 1
    else:
        right_score += 1

    if answers[10] == "+":
        liberal_score += 1
    else:
        authoritarian_score += 1

    total_score.append(right_score - left_score)
    total_score.append(authoritarian_score - liberal_score)
    total_score.append(economic_score - social_score)

    return 13


# То же самое - много копипасты(
async def score(update, context):
    global total_score
    global sc
    horizontal_score = total_score[0] + total_score[2]
    vertical_score = total_score[1]
    if vertical_score == 3  and horizontal_score <= 3 and horizontal_score >= 6:
        sc = 'авторитаризм'
    elif vertical_score == 1  and horizontal_score <= 3 and horizontal_score >= 6:
        sc = 'центризм'
    elif vertical_score == -1 and horizontal_score <= 3 and horizontal_score >= 6:
        sc = 'центризм'
    elif vertical_score == -3 and horizontal_score <= 3 and horizontal_score >= 6:
        sc = 'либерализм'
    elif vertical_score == 3 and horizontal_score > 4:
        sc = 'фашизм'
    elif vertical_score == 1 and horizontal_score > 4:
        sc = 'капитализм'
    elif vertical_score == -1 and horizontal_score > 4:
        sc = 'капитализм'
    elif vertical_score == -3 and horizontal_score > 4:
        sc = 'либертарианство'
    elif vertical_score == 3 and horizontal_score < 4:
        sc = 'коммунизм'
    elif vertical_score == 1 and horizontal_score < 4:
        sc = 'социал-демократия'
    elif vertical_score == -1 and horizontal_score < 4:
        sc = 'социал-демократия'
    elif vertical_score == -3 and horizontal_score < 4:
        sc = 'анархия'

    await update.message.reply_text(sc)

    sc = ''
    # Непонятно, зачем записывать 0 в переменные
    horizontal_score = 0
    vertical_score = 0
    total_score = []

    return 0


async def stop(update, context):
    global answers
    global question_number
    global sc
    sc = ''
    await update.message.reply_text("Всего доброго!")
    answers = []
    question_number = 0
    return ConversationHandler.END


def main():
    # [note] Отладочный print лучше убирать
    print(answers)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            8: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            9: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            10: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            11: [MessageHandler(filters.TEXT & ~filters.COMMAND, response)],
            12: [MessageHandler(filters.TEXT & ~filters.COMMAND, count)],
            13: [MessageHandler(filters.TEXT & ~filters.COMMAND, score)]

        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application = Application.builder().token(TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(CommandHandler("help", help))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
