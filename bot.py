import random
import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

group_id = 202195958
token = '47f55be410db4d49ec6441471538e98a39d040ae65e9cecfb8d17057f7f28ab010f6bef71ca6d37d8abb9'

log = logging.getLogger('bot')

def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.log', 'a', 'utf-8')
    file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


class Bot:

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug('Отправляем сообщение назад')
            self.api.messages.send(
                message=event.object.message['text'],
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.object.message["peer_id"],
            )
        else:
            log.info("Мы пока не умеем обрабатывать событие такого типа %s", event.type)

if __name__ == '__main__':
    configure_logging()
    bot = Bot(group_id, token)
    bot.run()



# event.object = {'message': {'date': 1611947405, 'from_id': 34855643, 'id': 30, 'out': 0, 'peer_id': 34855643, 'text': 'fdsafdsaf', 'conversation_message_id': 29, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'intent_subscribe', 'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': False, 'lang_id': 0}}