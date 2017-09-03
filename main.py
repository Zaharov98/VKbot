""" Zaharov I. 30.07.17
    Python 3.6.2 """


import vk
import threading
import json
import telebot

import logging as log
import traceback as tb

log.basicConfig(level=log.DEBUG, format=" %(asctime)s - %(levelname)s - %(message)s")
# logging.disable(logging.DEBUG)


access_token_tel = ""
bot = telebot.TeleBot(access_token_tel)
chat_id = 0
stream = {}


@bot.message_handler(commands=["vkset", ])
def bot_set_rule(msg):
    """set rule for vk stream"""
    try:
        rule, tag = msg.text.split()[1:3]
        vk_server_log = vk.set_rule(stream, rule, tag)

    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, e.__context__)
    else:
        log.debug(vk_server_log)
        bot.send_message(chat_id, vk_server_log)


@bot.message_handler(commands=["vkdel", ])
def bot_del_rule(msg):
    """delete rule, that seted to filter the stream"""
    try:
        tag = msg.text.split()[1]
        vk_server_log = vk.delete_rule(stream, tag)

    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, e.__context__)
    else:
        log.debug(vk_server_log)
        bot.send_message(chat_id, vk_server_log)


@bot.message_handler(commands=["vkget", ])
def bot_get_rules(msg):
    """send stream rules on chat"""
    try:
        vk_server_log = vk.get_rules(stream)

    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, e.__context__)
    else:
        log.debug(vk_server_log)
        bot.send_message(chat_id, vk_server_log)


@bot.message_handler(commands=["start", ])
def bot_start(msg):
    """starting telegram bot"""
    global chat_id
    chat_id = msg.chat.id

    greetings = "Hello, {}! I'm working now!".format(msg.from_user.first_name)
    bot.send_message(chat_id, greetings)
    # vk streaming api turning on
    vk_start()


def bot_stream_redirect(ws, msg):
    """redirect message stream to telegram chat.
    ws - WebSocket class"""
    vk_data = json.loads(msg)
    # TODO: Parse vk server message
    post = vk_data["event"]["text"].replace("<br>", "\n") + "\n" + vk_data["event"]["event_url"]
    log.debug(post)
    bot.send_message(chat_id, post)


def vk_start():
    """vk api turning on"""
    try:
        global stream
        stream = vk.get_server_streaming_key()

        message_thread = threading.Thread(target=vk.listen_stream, args=[stream, bot_stream_redirect, ])
        message_thread.daemon = True
        message_thread.start()
        message_thread.join()

    except Exception as e:
        # tb.print_tb(e)
        log.exception(e.__context__)


if __name__ == "__main__":
    bot.polling()

