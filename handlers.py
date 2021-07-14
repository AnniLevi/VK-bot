"""
Handler - функция, которая принимает на вход text (текст входящего сообщения) и context (dict),
а возвращает bool:
True - если шаг пройден,
False - если данные введены неверно.

"""

import re

from generate_ticket import generate_ticket

re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def handler_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handler_email(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = matches[0]
        return True
    else:
        return False


def handler_generate_ticket(text, context):
    return generate_ticket(name=context['name'], email=context['email'])
