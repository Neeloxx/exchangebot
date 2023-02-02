import telebot
from additions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Вас приветствует онлайн обменник!\
\nВся информация по работе бота записана тут --> /help"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в слудеющем формате: \n<имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>(через пробел)\
\nчтобы узнать все валюты нажми сюда ---> /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()