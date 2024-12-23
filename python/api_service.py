import requests

def get_bitcoin_price():
    """Получает текущую цену Bitcoin."""
    try:
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return None

def process_bitcoin_price(data):
    """Обрабатывает данные о цене Bitcoin."""
    if data and "bpi" in data and "USD" in data["bpi"]:
        price_data = data["bpi"]["USD"]
        return f"Current Bitcoin price: {price_data['rate']} {price_data['symbol']}"
    else:
        return "Невозможно получить цену Bitcoin"
