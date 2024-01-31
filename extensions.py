import requests
import json
from util import keys, API_KEY


class ConvertionException(Exception):
	pass


class CurrencyConvert:
	@staticmethod
	def get_price(quote: str, base: str, amount: str):
		if quote == base:
			raise ConvertionException(f"Невозможно перевести одинаковые валюты {base}")

		try:
			quote_ticker = keys[quote]
		except KeyError:
			raise ConvertionException(f"Не удалось обработать валюту {quote}")

		try:
			base_ticker = keys[base]
		except KeyError:
			raise ConvertionException(f"Не удалось обработать валюту {base}")

		try:
			amount = float(amount)
		except ValueError:
			raise ConvertionException(f"Не удалось обработать количество {amount}")

		api_url = f'https://api.getgeoapi.com/v2/currency/convert?\
api_key={API_KEY}&from={quote_ticker}&to={base_ticker}&amount=\
{amount}&format=json'
		r = requests.get(api_url)
		total_base = json.loads(r.content)['rates'][keys[base]]['rate_for_amount']
		return total_base
