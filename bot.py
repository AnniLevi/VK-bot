import random
import vk_api
import vk_api.bot_longpoll

group_id = 202195958
token = '47f55be410db4d49ec6441471538e98a39d040ae65e9cecfb8d17057f7f28ab010f6bef71ca6d37d8abb9'


class Bot:

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception as err:
                print(f'Ошибка: {err}')

    def on_event(self, event):
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            self.api.messages.send(
                message=event.object.message['text'],
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.object.message["peer_id"],
            )
        else:
            print("Мы пока не умеем обрабатывать событие такого типа", event.type)

if __name__ == '__main__':
    bot = Bot(group_id, token)
    bot.run()



# event.object = {'message': {'date': 1611947405, 'from_id': 34855643, 'id': 30, 'out': 0, 'peer_id': 34855643, 'text': 'fdsafdsaf', 'conversation_message_id': 29, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'intent_subscribe', 'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': False, 'lang_id': 0}}