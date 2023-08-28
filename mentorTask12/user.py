import attr
from camel_to_snake_converter import change_case


@attr.s
class User:
    u_name: str = attr.ib(default="uid2000")
    email: str = attr.ib(default="a@gmail.com")
    f_name: str = attr.ib(default="un sn")
    hash_pass: str = attr.ib(default='1234')

    def __setattr__(self, __name: str, __value) -> None:
        __name = change_case(__name)

        if __name == "u_name":
            self.__dict__[__name] = __value
        elif __name == "email":
            self.__dict__[__name] = __value
        elif __name == "f_name":
            self.__dict__[__name] = __value
        elif __name == "hash_pass":
            self.__dict__[__name] = __value
