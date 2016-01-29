import logging
from time import sleep
from telegram import Updater
from telegram import ReplyKeyboardMarkup

job_queue = None
signal = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    chat_id = update.message.chat_id
    text = "Start timer whenever you want"
    custom_keyboard = [['Время!', 'Сброс']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    bot.sendMessage(chat_id=chat_id, text=text, reply_markup=reply_markup)


def start_timer(bot, update):
    chat_id = update.message.chat_id

    bot.sendMessage(chat_id, 'Время пошло!')

    def ten_seconds(bot):
        if not signal.get(chat_id, None):
            bot.sendMessage(chat_id, '10 секунд')

    def time_is_up(bot):
        if not signal.get(chat_id, None):
            bot.sendMessage(chat_id, 'Время!')
            for i in range(10, 0, -1):
                sleep(1)
                bot.sendMessage(chat_id, str(i))
            sleep(1)
            bot.sendMessage(chat_id, "Все ответы должны быть сданы")
        else:
            signal[chat_id] = False

    job_queue.put(ten_seconds, 50, repeat=False)
    job_queue.put(time_is_up, 60, repeat=False)


def cancel(bot, update):
    chat_id = update.message.chat_id
    signal[chat_id] = True
    bot.sendMessage(chat_id, "Таймер сброшен")


def any_message(bot, update):
    if update.message.text == 'Время!':
        start_timer(bot, update)
    if update.message.text == 'Сброс':
        cancel(bot, update)


def main():
    global job_queue
    token = '142603543:AAGjbFCNsRAsnNbueaF19UuGrjhEgvDqbpY'
    updater = Updater(token)
    job_queue = updater.job_queue

    dp = updater.dispatcher

    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("start_timer", start_timer)
    dp.addTelegramCommandHandler("cancel", cancel)
    dp.addTelegramMessageHandler(any_message)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
