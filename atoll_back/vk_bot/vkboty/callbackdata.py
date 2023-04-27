import json


class CallbackDataJson:

    @staticmethod
    def new(prefix: str, **kwargs) -> str:
        data = {'prefix': prefix}
        data.update(kwargs)
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def check_prefix(prefix: str, callback_data: dict):
        if not callback_data:
            return False

        if callback_data.get('prefix') and callback_data.get('prefix') == prefix:
            return True
        return False
