import random
import logging

import handlers
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

try:
    import settings
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')

log = logging.getLogger('bot')


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.log', 'a', 'utf-8')
    file_handler.setFormatter(
        logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)

class UserState:
    """
    Состояние пользоваетля внутри сценария
    """

    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}

class Bot:
    '''
    Use Python 3.9.1
    Сценарий регистрации на конференицию через vk.com.

    Поддерживает ответы на вопросы про дату, место проведения и сценарий реигстрации:
    - спрашивает ит
    - спрашивает e-mail
    - говорит об успешной регистрации
    Если шаг не пройден, задает уточнющий вопрос, пока шаг не будет пройден.
    '''

    def __init__(self, group_id, token):
        '''
        :param group_id: group id from vk group
        :param token: secret token
        '''
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.user_states = dict()  # user_id -> UserState

    def run(self):
        '''Bot launch'''
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        '''
        Регистрация на конференцию
        :param event: VkBotMessageEvent object
        :return: None
        '''
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info("Мы пока не умеем обрабатывать событие такого типа %s", event.type)
            return
        user_id = event.object.message["peer_id"]
        text = event.object.message["text"]
        if user_id in self.user_states:
            text_to_send = self.continue_scenario(user_id, text)
        else:
            # search intent
            for intent in settings.INTENTS:
                log.debug(f'User gets {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    # run intent
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(user_id, intent['scenario'])
                    break
            else:
                text_to_send = settings.DEFAULT_ANSWER

        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id,
        )

    def start_scenario(self, user_id, scenario_name):
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            # next step
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                log.info('Зарегистрирован: {name} {email}'.format(**state.context))
                self.user_states.pop(user_id)
        else:
            # retry current step
            text_to_send = step['failure_text'].format(**state.context)
        return text_to_send


if __name__ == '__main__':
    configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()

# event.object = {'message': {'date': 1611947405, 'from_id': 34855643, 'id': 30, 'out': 0, 'peer_id': 34855643, 'text': 'fdsafdsaf', 'conversation_message_id': 29, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'intent_subscribe', 'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': False, 'lang_id': 0}}
