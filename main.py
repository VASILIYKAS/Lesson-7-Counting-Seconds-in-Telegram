import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv


# Обрабатывает входящие сообщения, запускает таймер и отправляет уведомления
def reply(chat_id, text, bot):
    time_in_seconds = parse(text)
    msg_id = bot.send_message(chat_id, "Таймер запущен на {} секунд.".format(time_in_seconds))
    bot.create_countdown(time_in_seconds, notify_progress, chat_id=chat_id,
                         msg_id=msg_id, time_in_seconds=time_in_seconds, bot=bot)
    bot.create_timer(time_in_seconds, end,
                     chat_id=chat_id, bot=bot)


# Обновляет сообщение с оставшимся временем и прогресс-баром
def notify_progress(secs_left, chat_id, msg_id, time_in_seconds, bot):
    times_bar = time_in_seconds - secs_left
    bot.update_message(chat_id, msg_id,
                       "Осталось секунд {} \n{}".format(secs_left, render_progressbar(time_in_seconds, times_bar)))


# Создает строку прогресс-бара
def render_progressbar(total, iteration, prefix='', suffix='', length=20, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


# Отправляет сообщение о завершении таймера
def end(chat_id, bot):
    bot.send_message(chat_id, "Время вышло")


def main():
    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
