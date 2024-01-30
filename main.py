import requests
import telebot
import json

TOKEN = '6895653645:AAF6njjvsfEb1QWGqXMJFoOufxj79ivxa40'

API_KEY = '280cf57a5643b6a73b6f8a010846380e2072540d'


bot = telebot.TeleBot(TOKEN)

keys = {
	'рубль': 'RUB',
	'доллар': 'USD',
	'евро': 'EUR',
	'тенге': 'KZT',
	'фунт': 'GBP',
	'донг': 'VND',
	'бат': 'THB',
	'йена': 'JPY',
}


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
	quote, base, amount = message.text.split(' ')
	api_url = f'https://api.getgeoapi.com/v2/currency/convert?\
api_key={API_KEY}&from={keys[quote]}&to={keys[base]}&amount=\
{amount}&format=json'
	r = requests.get(api_url)
	answer = json.loads(r.content)['rates'][keys[base]]['rate_for_amount']
	bot.send_message(message.chat.id, answer)


bot.polling()
