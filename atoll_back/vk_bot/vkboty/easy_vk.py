from types import SimpleNamespace
from typing import Optional

from vk_api.keyboard import VkKeyboard
from vk_api.vk_api import VkApiMethod

DEFAULT_USER_DATA_FIELDS = ['city', 'can_see_audio', 'first_name', 'last_name', 'is_closed']


class EasyVk:
    MAX_MSG_SIZE = 4096

    def __init__(self, vk_api: VkApiMethod):
        self.vk_api = vk_api

    def send_msg(self, user_id, message: str, keyboard: VkKeyboard = None, **kwargs):
        kwargs['user_id'] = user_id
        kwargs['message'] = message
        kwargs['keyboard'] = keyboard
        if not kwargs.get('random_id'):
            kwargs['random_id'] = 0
        return self.vk_api.messages.send(**kwargs)

    def send_callback_answer(self, event_id: str, user_id: str, peer_id: str, event_data=None):
        self.vk_api.messages.sendMessageEventAnswer(event_id=event_id, user_id=user_id,
                                                    peer_id=peer_id, event_data=event_data)

    def set_typing(self, user_id):
        self.vk_api.messages.setActivity(user_id=user_id, type='typing')

    def user_data(self, user_id, fields=None) -> Optional[SimpleNamespace]:
        if fields is None:
            fields = DEFAULT_USER_DATA_FIELDS
        res = list(self.vk_api.users.get(user_ids=user_id, fields=','.join(fields)))
        if not res:
            return None
        return SimpleNamespace(**res[0])
