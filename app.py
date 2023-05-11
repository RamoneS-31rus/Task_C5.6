import telebot

from config import CURRENCY_LIST, TOKEN
from extensions import ConvertException, Convert


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def get_help(message: telebot.types.Message):
    text = 'Формат ввода: \n\
<базовая валюта> <котируемая валюта> <количество базовой валюты>  \n\
Пример ввода: доллар рубль 1 \n\
Список команд: \n\
/values - доступные валюты'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def get_currency_list(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in CURRENCY_LIST.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertException('Некорректное количество параметров.')
        else:
            base, quote, amount = values

        conversion_result = Convert.get_price(base, quote, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'{amount} {CURRENCY_LIST[base]} = {conversion_result} {CURRENCY_LIST[quote]}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
