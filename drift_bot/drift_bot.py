# -*- coding: utf-8 -*-
from telegram import Updater
from datetime import datetime
import logging

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

work = dict()
job_queue = None


def is_good_time():
    """
    :return: True if day is working day and time is between 9:00 and 19:00
    """
    d = datetime.today()
    if d.weekday() in [5, 6]:
        return False
    if d.timetuple()[3] < 9 or d.timetuple()[3] > 18:
        return False
    return True


def start(bot, update, args):
    chat_id = update.message.chat_id
    try:
        interval = int(args[0])
    except IndexError:
        interval = 7200
    except ValueError:
        bot.sendMessage(chat_id, text=u'Укажите корректный интервал')
        return

    if chat_id in work:
        work[chat_id] += 1
    else:
        work[chat_id] = 1

    job_number = work[chat_id]

    def alarm(bot):
        if job_number != work[chat_id]:
            return
        if is_good_time():
            bot.sendMessage(chat_id=chat_id, text="Пора")
        job_queue.put(alarm, interval, repeat=False)

    job_queue.put(alarm, interval, repeat=False)
    bot.sendMessage(chat_id, "Таймер установлен")


def stop(bot, update):
    work[update.message.chat_id] = 0
    bot.sendMessage(update.message.chat_id, "Не задохнитесь без меня!")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    global job_queue

    updater = Updater(token='145193673:AAGX8s8NQFqJTbbi1ZAEuhjVxstToboziw8')
    job_queue = updater.job_queue

    dp = updater.dispatcher

    dp.addTelegramCommandHandler('start', start)
    dp.addTelegramCommandHandler('stop', stop)
    dp.addErrorHandler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
