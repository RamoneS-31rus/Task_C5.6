import requests
import json
from config import API_KEY, CURRENCY_LIST


class ConvertException(Exception):
    pass


class Convert:

    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise ConvertException(f'Нельзя конвертировать "{base}" в "{base}".')

        try:
            base_code = CURRENCY_LIST[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту "{base}".')

        try:
            quote_code = CURRENCY_LIST[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту "{quote}".')

        try:
            if float(amount) > 0:
                amount = float(amount)
            else:
                raise ConvertException(f'Не удалось обработать количество "{amount}".')
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество "{amount}".')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_code}/{quote_code}/{amount}')

        conversion_result = json.loads(r.content)['conversion_result']

        return conversion_result
