from typing import Union

from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEventType, VkBotEvent


class Filters:
    @staticmethod
    def is_from_user(e: Union[VkBotEvent, VkBotMessageEvent]):
        if e.type == VkBotEventType.MESSAGE_NEW or e.type == VkBotEventType.MESSAGE_EVENT:
            return True

    @staticmethod
    def is_text_message(e: VkBotMessageEvent):
        if not isinstance(e, VkBotMessageEvent):
            return False

        if e.type == VkBotEventType.MESSAGE_NEW and e.from_user and e.message.text:
            return True

    @staticmethod
    def is_callback_payload(e: VkBotEvent):
        if not isinstance(e, VkBotEvent):
            return False

        if e.type == VkBotEventType.MESSAGE_EVENT and e.object.payload:
            return True
