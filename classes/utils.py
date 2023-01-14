import hashlib
from dateutil import parser
from loguru import logger
import re


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_attr_try(obj, attr):
        try:
            return getattr(obj, attr)
        except Exception as e:
            logger.error(f"Error getting the obj attribute {attr}\n{e}")

    @staticmethod
    def str_to_float_arr(value: str):
        arr = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", value)
        return [float(x) for x in arr]

    @staticmethod
    def str_to_float(
        value: str, raise_errors: bool = False, *, default_value: float = None
    ) -> float:
        if isinstance(value, int):
            return float(value)
        elif isinstance(value, float):
            return value

        arr = str_to_float_arr(value)

        if len(arr) == 0:
            if default_value:
                return default_value
            elif raise_errors:
                raise ValueError("`value` does not convert to float")
            else:
                return None
        elif len(arr) > 1:
            if raise_errors:
                raise ValueError("`value` does not convert to float")
            else:
                return None
        else:
            return float(arr[0])

    @staticmethod
    def int_from_str(text_, default_for_none=None):
        numbers = re.findall("\d+", text_)
        if len(numbers) == 0:
            return default_for_none
        elif len(numbers) == 1:
            return numbers[0]
        else:
            raise ValueError("String with multiple numbers")

    @staticmethod
    def parse_date(text_):
        if text_ is None:
            return None
        return parser.parse(text_, dayfirst=True)

    @staticmethod
    def md5(s: str) -> str:
        return hashlib.md5(s.encode("utf-8")).hexdigest()
