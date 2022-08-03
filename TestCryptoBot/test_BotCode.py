import unittest
from unittest.mock import Mock
from unittest.mock import patch
from CryptoBot.BotCode import user, currency_price
import requests_mock

# requests.get = Mock('/Users/vadim/Documents/BotProject/currency_price.json')

class BotTest(unittest.TestCase):
    def test_get_balance(self):
        vadim = user("Vadim")
        self.assertEqual(vadim.get_balance()['USD'], 10000.0)

    
    @patch('requests.get')
    def test_buy(self, mocked_get):
        mocked_get.return_value.json.return_value = { "data" : {"priceUsd" : "10000.0"} }
        response = currency_price('bitcoin')
        self.assertEqual(response, '10000.0')
        vadim = user("Vadim")
        vadim.buy('BTC', 'USD', 0.1)
        self.assertEqual(vadim.get_balance()['BTC'], 0.1)
        #self.assertEqual(mocked_get.get_balance()['USD'], 9000)
        
        
        
        
        
        
        
        
        
        
        
        #with requests_mock.Mocker() as rm:
           #rm.get(('https://api.coincap.io/v2/assets/bitcoin'), json = {"data" : {"priceUsd" : "10000.0"} }, status_code=200)
           # json = {"data" : {"priceUsd" : "10000.0"} }
           # response = currency_price('bitcoin')
            #self.assertEqual(response, '10000.0')
            #vadim = user("Vadim")
            #vadim.buy('BTC', 'USD', 0.1)
            #self.assertEqual(vadim.get_balance()['BTC'], 0.1)
            #self.assertEqual(vadim.get_balance()['USD'], 9000)
        
        
        
        
        
         #with requests_mock.Mocker() as rm:
            #rm.get('https://api.coincap.io/v2/assets/bitcoin', json = {"data" : {"priceUsd" : "10000.0"} }, status_code=200)
            #response = currency_price('bitcoin')
            #self.assertEqual(response, '10000.0')


    #def test_buy(self):
        #with requests_mock.Mocker() as rm:
            #rm.get('https://api.coincap.io/v2/assets/bitcoin', json = {"data" : {"priceUsd" : "10000.0"} }, status_code=200)
            #response = currency_price('bitcoin')
            #self.assertEqual(response, '10000.0')
            #vadim = user("Vadim")
            #vadim.buy('BTC', 'USD', 0.1)
            #self.assertEqual(vadim.get_balance()['BTC'], 0.1)
            #self.assertEqual(vadim.get_balance()['USD'], 9000)


    #@patch('requests.get')
    #def test_buy(mocked_get):
       #mocked_get.return_value.status_code.return_value = 200
        #mock_get.return_value.json.return_value = { "data" : {"priceUsd" : 10000} }
        #self.assertEqual(1, 1)
        #vadim = user("Vadim")
        #vadim.buy('BTC', 'USD', 0.1)
        #self.assertEqual(vadim.get_balance()['BTC'], 0.1)
        #self.assertEqual(vadim.get_balance()['USD'], 9000)
        #vadim.get_balance()
        #self.assertEqual(vadim.get_balance(), dict)

if __name__ == "__main__":
    unittest.main()