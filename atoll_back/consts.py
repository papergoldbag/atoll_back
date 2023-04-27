from typing import Union

from atoll_back.helpers import SetForClass


class MailCodeTypes(SetForClass):
    reg = "reg"
    auth = "auth"


class UserRoles(SetForClass):
    default = "default"
    admin = "admin"


RolesType = Union[set[str], list[str], str]


class Modes(SetForClass):
    prod = "prod"
    dev = "dev"


class TgBotCommands(SetForClass):
    start = "start"
    echo = "echo"
