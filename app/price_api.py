import requests


# API request for currency price

def currency_price(currency):
    service_url = 'https://api.coinpaprika.com/v1/tickers/'
    url = service_url + currency
    response = requests.get(url)
    js = response.json()
    return (js["quotes"]["USD"]["price"])

currency_prices = {
  'USDT' : 1,
  'BTC' : float(currency_price('btc-bitcoin')), 
  'ETH' : float(currency_price('eth-ethereum')), 
  'ANT' : float(currency_price('ant-aragon')), 
  'SOL' : float(currency_price('sol-solana')), 
  'DOGE' : float(currency_price('doge-dogecoin'))
  }
