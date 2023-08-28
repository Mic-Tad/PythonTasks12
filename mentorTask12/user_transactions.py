import attr
from camel_to_snake_converter import change_case


@attr.s
class UsersTransactions:
    u_name: str = attr.ib(default="uid2000")
    transactions: list = attr.ib(default=[])

    def __setattr__(self, __name: str, __value) -> None:
        __name = change_case(__name)
        self.__dict__[__name] = __value


