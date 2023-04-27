import logging
import time
from typing import Callable, Union

from requests import Session
from requests.adapters import HTTPAdapter
from schedule import Scheduler
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotMessageEvent
from vk_api.vk_api import VkApiMethod

from atoll_back.vk_bot.vkboty.easy_vk import EasyVk
from atoll_back.vk_bot.vkboty.memory import Memory
from atoll_back.vk_bot.vkboty.threader import Threader

logger = logging.getLogger(__name__)


class Actions:
    NextHandler = 'next_handler'


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
)


class VkBoty:
    def __init__(self, token: str, group_id: str, api_version: str = "5.131"):
        __session = Session()
        __adapter = HTTPAdapter(max_retries=15)
        __session.mount("http://", __adapter)
        __session.mount("https://", __adapter)
        __session.headers["user-agent"] = USER_AGENT
        self.vk_session = VkApi(token=token, session=__session, api_version=api_version)
        self.vk_longpoll = VkBotLongPoll(self.vk_session, group_id, wait=25)
        self.vk_api: VkApiMethod = self.vk_session.get_api()
        self.threader = Threader()
        self.memory = Memory()
        self.__handlers = []
        self.on_startups = []
        self.on_shutdowns = []
        self.__error_handler = None
        self.easy_vk = EasyVk(self.vk_api)
        self.scheduler = Scheduler()

    def handler(self, *custom_filters: Callable[[Union[VkBotEvent, VkBotMessageEvent]], bool]):
        def wrapper(callback: Callable[[Union[VkBotEvent, VkBotMessageEvent]], bool]):
            def handler(e: Union[VkBotEvent, VkBotMessageEvent]):
                for cf in custom_filters:
                    if not cf(e):
                        return Actions.NextHandler
                return callback(e)

            self.__handlers.append(handler)

        return wrapper

    def add_handler(self, callback: Callable[[Union[VkBotEvent, VkBotMessageEvent]], bool],
                    *custom_filters: Callable[[Union[VkBotEvent, VkBotMessageEvent]], bool]):
        def handler(e: Union[VkBotEvent, VkBotMessageEvent]):
            for cf in custom_filters:
                if not cf(e):
                    return Actions.NextHandler
            return callback(e)

        self.__handlers.append(handler)

    def __handle(self, e: Union[VkBotEvent, VkBotMessageEvent]):
        for handler in self.__handlers:
            try:
                action = handler(e)
            except Exception as err:
                action = self.__error_handler(e, err)

            if action == Actions.NextHandler:
                continue
            else:
                break

    def error_handler(self):
        def wrapper(callback: Callable[[Union[VkBotEvent, VkBotMessageEvent], Exception], None]):
            self.__error_handler = callback

        return wrapper

    def add_err_handler(self, callback: Callable[[Union[VkBotEvent, VkBotMessageEvent], Exception], None]):
        self.__error_handler = callback

    def __run_schedule(self):
        while True:
            self.scheduler.run_pending()
            time.sleep(5)

    def on_startup(self, func, *args, **kwargs):
        self.on_startups.append((func, args, kwargs))

    def listen_and_handle_events(self):
        for e in self.vk_longpoll.listen():
            future = self.threader.start_new(self.__handle, e)
            exc = future.exception()
            if exc:
                logger.exception("exception in a handling thread", exc_info=exc)

    def start(self):
        logger.info('start')
        for f, args, kwargs in self.on_startups:
            f(*args, **kwargs)
        logger.info('on_startups were done')

        self.threader.start_new(self.__run_schedule)
        logger.info('scheduler was started')
        logger.info('listening events')
        try:
            self.listen_and_handle_events()
        except Exception as e:
            logger.error(e)
            self.stop()

    def stop(self):
        logger.info('stopping')
        for j in self.scheduler.jobs:
            self.scheduler.cancel_job(j)
        del self.scheduler  # we need to do this
        self.threader.stop()
