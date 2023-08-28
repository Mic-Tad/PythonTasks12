import attr
from camel_to_snake_converter import change_case
from cl_currency import ClCurrency
from statuses import Status


@attr.s
class TransactionDetails:
    transaction_id: str = attr.ib(default="tid2000")
    transaction_status: Status = attr.ib(default=Status.Successful)
    amount: int = attr.ib(default=0)
    currency: ClCurrency = attr.ib(default=ClCurrency.USD)
    recipient_u_name: str = attr.ib(default="uid2000")

    def __setattr__(self, __name: str, __value) -> None:
        __name = change_case(__name)
        if __name == "transaction_id":
            self.__dict__[__name] = __value
        elif __name == "amount":
            self.__dict__[__name] = int(__value)
        elif __name == "currency":
            if type(__value) == str:
                __value = ClCurrency[__value]
            self.__dict__[__name] = __value
        elif __name == "transaction_status":
            if type(__value) == str:
                __value = Status[__value]
            self.__dict__[__name] = __value
        elif __name == "recipient_u_name":
            self.__dict__[__name] = __value
