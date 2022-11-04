import requests


request_url = "https://api.coingecko.com/api/v3/coins/list?include_platform=false"

response = requests.get((request_url))
data = response.json()

symbols_to_ids = {item['symbol']: item['id'] for item in data}
symbols_to_ids['btc']


def get_symbol_price(symbol: str) -> float:
    token_symbol, notional = symbol.split('/')
    id_ = symbols_to_ids[token_symbol.lower()]
    request_url = f'https://api.coingecko.com/api/v3/simple/price?ids={id_}&vs_currencies={notional.lower()}'
    
    return requests.get(request_url).json()[id_][notional.lower()]