""" VK-streaming-API interface
    Zaharov I. 29.08.17
    Python 3.6.2
    VK token 3a665aea3a665aea3a665aeac73a3bd74e33a663a665aea631bf34c8f38de9b4ddbc1b2
    [{'tag': '27', 'value': 'кот'}, {'tag': '28', 'value': 'vk'}, {'tag': '35', 'value': 'кот'}]"""


import json
import requests
import websocket

import logging as log


_access_token_vk = "3a665aea3a665aea3a665aeac73a3bd74e33a663a665aea631bf34c8f38de9b4ddbc1b2"


def get_server_streaming_key():
    """getting VK server handle"""
    request_url = "https://api.vk.com/method/streaming.getServerUrl?access_token={}&v=5.64".format(_access_token_vk)
    log.debug("Request URL: " + request_url)

    r = requests.get(request_url)
    data = r.json()
    return {"server": data["response"]["endpoint"], "key": data["response"]["key"]}


def get_rules(stream):
    """"""
    try:
        r = requests.get("https://{}/rules?key={}".format(stream["server"], stream["key"]))
        data = r.json()

    except Exception as e:
        #tb.print_tb(e)
        log.exception(e.__context__)
    else:

        if data["code"] == 200:
            return data["rules"]
        elif data["code"] == 400:
            log.error(data["error"]["message"] + " : " + str(data["error"]["error_code"]))


def set_rule(stream, rule, rule_tag):
    """set criterion's for sending posts
    send http POST request"""
    try:
        rule_params = {"rule": {"value": rule,  "tag": str(rule_tag)}}
        headers = {"Content-Type": "application/json"}
        r = requests.post(url="https://{}/rules?key={}".format(stream["server"], stream["key"]),
                          data=json.dumps(rule_params), headers=headers)
        data = r.json()

    except Exception as e:
        #tb.print_tb(e)
        log.exception(e.__context__)
    else:

        if data["code"] == 400:
            return str(data["error"]["message"] + " : " + str(data["error"]["error_code"]))
        elif data["code"] == 200:
            return str("rule " + rule + " added!")


def delete_rule(stream, rule_tag):
    """delete one of the criterion's for
    sending posts. send http delete request"""
    try:
        del_params = {"tag": str(rule_tag)}
        headers = {"Content-Type": "application/json"}
        r = requests.delete(url="https://{}/rules?key={}".format(stream["server"], stream["key"]),
                            data=json.dumps(del_params), headers=headers)
        data = r.json()

    except Exception as e:
        log.exception(e.__context__)
    else:

        if data["code"] == 200:
            return str("rule " + str(rule_tag) + " deleted!")
        elif data["code"] == 400:
            return data["error"]["message"] + " : " + str(data["error"]["error_code"])


def listen_stream(stream, on_message=None):
    """getting massages from VK server"""
    headers = {"Connection": "upgrade", "Upgrade": "websocket", "Sec-Websocket-Version": "13"}
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://{}/stream?key={} ".format(stream["server"], stream["key"]),
                                on_message=on_message if on_message else _on_message, on_error=_on_error,
                                on_close=_on_close, header=headers)
    ws.on_open = _on_open
    ws.run_forever()


def _on_message(ws, message):
    """VK post processing and formatting"""
    message = json.loads(message)

    # TODO: Parse vk server message
    post = message["event"]["event_type"] + "\n" +\
            message["event"]["text"].replace("<br>", "\n") +\
            message["event"]["event_url"] + "\n"

    log.debug(post)


def _on_error(ws, error):
    """"""
    log.debug("Error thead: ", error)


def _on_close(ws, ):
    """"""
    log.debug("Close thead...")


def _on_open(ws, ):
    """"""
    log.debug("Open thead...")