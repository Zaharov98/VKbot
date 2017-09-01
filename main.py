""" Zaharov I. 30.07.17
    Python 3.6.2 """


import vk
import threading
import telebot

import logging as log
import traceback as tb

log.basicConfig(level=log.DEBUG, format=" %(asctime)s - %(levelname)s - %(message)s")
# logging.disable(logging.DEBUG)


access_token_tel = "415697146:AAHAKG3tT06WvyUIk1kabVJV7HE_YIYnoJ4"
bot = telebot.TeleBot(access_token_tel)


@bot.message_handler(commands=["start", ])
def bot_start(msg):
    """starting telegram bot"""
    global chat_id
    chat_id = msg.chat.id

    greetings = "Hello, {}! I'm working now!".format(msg.from_user.first_name)
    bot.send_message(chat_id, greetings)
    # vk streaming api turning on
    vk_start()


def vk_start():
    """vk api turning on"""
    try:
        stream = vk.get_server_streaming_key()
        message_thread = threading.Thread(target=vk.listen_stream, args=[stream, ])
        message_thread.daemon = True
        message_thread.start()
        message_thread.join()

    except Exception as e:
        # tb.print_tb(e)
        log.exception(e.__context__)


if __name__ == "__main__":
    bot.polling()

