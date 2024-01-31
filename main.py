import telebot
from extensions import ConvertionException, CurrencyConvert
from util import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def handle_start_help(message):
	if message.text == '/start':
		bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}, \
чтобы узнать о функциях бота воспользуйся командой /help')
	elif message.text == '/help':
		bot.send_message(message.chat.id, f'Чтобы узнать курс валют введи запрос в формате: \
<имя валюты> \
<валюта в которую преревести> \
<количество переводимой валюты> \
чтобы ознакомиться со списком валют введи /values')


@bot.message_handler(commands=['values'])
def values(message):
	text = 'Доступные валюты:'
	for key in keys.keys():
		text = '\n'.join((text, key, ))
	bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message):
	try:
		value = message.text.lower().split(' ')
		if len(value) != 3:
			raise ConvertionException("Слишком много параметров")

		quote, base, amount = value
		answer = CurrencyConvert.get_price(quote, base, amount)
	except ConvertionException as e:
		bot.reply_to(message, f"Ошибка пользователя.\n{e}")
	except Exception as e:
		bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
	else:
		bot.send_message(message.chat.id, f'Цена {amount} {quote} в {base} - {answer}')


bot.polling()
