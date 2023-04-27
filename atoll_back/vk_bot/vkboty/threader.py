import random
from concurrent.futures import ThreadPoolExecutor, Future
from datetime import datetime


class Threader:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=32)
        self.__key_to_future = {}

    def start_new(self, func, *args, **kwargs) -> Future:
        f = self.executor.submit(func, *args, **kwargs)
        return f

    def save(self, future: Future, key: str = None) -> str:
        if key in self.__key_to_future:
            raise ValueError('this key already exists')
        if not key:
            key = str(datetime.now().timestamp() + random.randint(1, 1000000))
        self.__key_to_future[key] = future
        return key

    def stop(self):
        self.executor.shutdown(False, cancel_futures=False)
