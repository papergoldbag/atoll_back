import copy
from typing import Union, Any, Optional


class Memory:
    def __init__(self):
        self.__data = {}

    def __create_if_not(self, user_id: Union[str, int]):
        if user_id not in self.__data:
            self.__data[user_id] = {}

    def set(self, user_id: Union[str, int], data: dict):
        if not data:
            data = {}
        else:
            data = copy.copy(data)
        self.__data[user_id] = data

    def update_data(self, user_id: Union[str, int], data: dict = None, **kwargs):
        self.__create_if_not(user_id)
        if data:
            self.__data[user_id].update(**copy.copy(data))
        self.__data[user_id].update(**copy.copy(kwargs))

    def get(self, user_id: Union[str, int]) -> dict:
        return copy.copy(self.__data.get(user_id))

    def get_data(self, user_id: Union[str, int], key) -> Any:
        if user_id not in self.__data:
            return None
        return copy.copy(self.get(user_id).get(key))

    def set_state(self, user_id: Union[str, int], state: Optional[str]):
        self.__create_if_not(user_id)
        self.__data[user_id]['state'] = state

    def get_state(self, user_id: Union[str, int]) -> Optional[str]:
        if user_id not in self.__data:
            return None
        return self.__data[user_id].get('state')

    def clear(self):
        self.__data.clear()
