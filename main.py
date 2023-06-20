
# Подключение библиотеки для работы с телеграм ботом
import telebot
from config import keys, TOKEN
from extensions import APIException, get_price

bot = telebot.TeleBot(TOKEN)


# Описание комманд /start и /help
@bot.message_handler(commands=['start','help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n <имя валюты>' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты>\nУвидить список всех доступных валют: /values'
    bot.reply_to(message, text)

# Описание комманды /values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = get_price.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # Для осуществления умножения переводим переменную amount из str в float
        final_price = total_base * float(amount)
        text = f'Цена {amount} {quote} в {base} - {final_price}'

        bot.send_message(message.chat.id, text)

bot.polling()