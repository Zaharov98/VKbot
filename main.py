""" Zaharov I. 13.10.17
    Python 3.6.2 """

# TODO: sending exceptions context into chat
# TODO: Parse vk server message


import datetime
import telebot
import threading
import io
import json

import logging as log
import traceback as tb

import vk
import grsu
import tokens


log.basicConfig(level=log.DEBUG, format=" %(asctime)s - %(levelname)s - %(message)s")
# logging.disable(logging.DEBUG)


access_token_tel = tokens.tb
bot = telebot.TeleBot(access_token_tel)
chat_id = 0
stream = {}


""" functions, that process commands for 
    VK streaming API using """


@bot.message_handler(commands=["vkset", ])
def bot_set_rule(msg):
    """ set rule for vk stream """
    try:
        rule, tag = msg.text.split()[1:3]
        vk_server_log = vk.set_rule(stream, rule, tag)

    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, "Exception")
    else:
        log.debug(vk_server_log)
        bot.send_message(chat_id, vk_server_log)


@bot.message_handler(commands=["vkdel", ])
def bot_del_rule(msg):
    """ delete rule, that seted to filter the stream """
    try:
        tag = msg.text.split()[1]
        vk_server_log = vk.delete_rule(stream, tag)

    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, "Exception")
    else:
        log.debug(vk_server_log)
        bot.send_message(chat_id, vk_server_log)


@bot.message_handler(commands=["vkget", ])
def bot_get_rules(msg):
    """ send stream rules on chat """
    try:
        vk_stream_rules = vk.get_rules(stream)

    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, "Exception")
    else:
        log.debug(vk_stream_rules)
        bot.send_message(chat_id, vk_stream_rules)


def bot_VKstream_redirect(ws, msg):
    """ redirect message stream to telegram chat.
        ws - WebSocket class """
    try:
        vk_data = json.loads(msg)
        post = vk_data["event"]["text"].replace("<br>", "\n") + "\n" + vk_data["event"]["event_url"]
        log.debug(post)
        bot.send_message(chat_id, post)
    except Exception as e:
        log.exception(e.__context__)


def vk_start():
    """ vk api turning on """
    try:
        global stream
        stream = vk.get_server_streaming_key()

        message_thread = threading.Thread(target=vk.listen_stream, args=[stream, bot_VKstream_redirect, ])
        message_thread.daemon = True
        message_thread.start()
        message_thread.join()

    except Exception as e:
        # tb.print_tb(e)
        log.exception(e.__context__)
        bot.send_message(chat_id, "Exception")


""" functions, that process commands
    for GrSU scheduler API """


@bot.message_handler(commands=["grsu_faculties", ])
def bot_get_faculty(msg):
    """ send GrSU faculties names and ID-s in chat """
    try:
        text = "\n".join([str(faculty) for faculty in grsu.get_faculties_list()])
        bot.send_message(chat_id, text)
    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, "Exception")


@bot.message_handler(commands=["grsu_groups", ])
def bot_get_groups(msg):
    """"""
    try:
        text = "\n".join([str(group) for group in grsu.get_groups_list(*msg.text.split()[1:3])])
        bot.send_message(chat_id, text)
    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, "Exception!")


@bot.message_handler(commands=["grsu_schedule"])
def bot_get_schedule(msg):
    """"""
    try:
        text = io.StringIO()
        for day in grsu.get_group_schedule(*msg.text.split()[1:4]):
            date = datetime.date(*[int(date) for date in day["date"].split('-')])
            text.write(str(date) + "\n")

            for lesson in day["lessons"]:
                text.write("  ".join([" - ".join([str(lesson["timeStart"]), str(lesson["timeEnd"])]),
                            " - ".join([str(lesson["address"]), str(lesson["room"])]), "\n", str(lesson["title"]),
                            str(lesson["teacher"]["fullname"]), "\n", ]))

            bot.send_message(chat_id, text.getvalue())
            # TODO: text buffer doesnt flushed
            text.flush()
    except Exception as e:
        log.exception(e.__context__)
        bot.send_message(chat_id, "Exception while schedule getting")


@bot.message_handler(commands=["start", ])
def bot_start(msg):
    """ starting telegram bot """
    global chat_id
    chat_id = msg.chat.id

    greetings = "Hello, {}! I'm working now!".format(msg.from_user.first_name)
    bot.send_message(chat_id, greetings)
    # vk streaming api turning on
    vk_start()


def main():
    """"""
    while True:
        try:
            bot.polling()
        except Exception as e:
            globals()["bot"] = telebot.TeleBot(access_token_tel)

            log.exception(e.__context__)
            bot.send_message(chat_id, "main Exception")


if __name__ == "__main__":
    main()

