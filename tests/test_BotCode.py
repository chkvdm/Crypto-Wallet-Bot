import unittest
from App_Code.BotCode import user, currency_price
from unittest.mock import patch

class BotTest(unittest.TestCase):
    def test_get_balance(self):
        vadim = user("Vadim")
        self.assertEqual(vadim.get_balance()['USD'], 10000.0)

    @patch("requests.get")
    def test_currency_price(self, mocked_get):
        mocked_get.return_value.json.return_value = { "data" : {"priceUsd" : "10000.0"} }
        response = currency_price('bitcoin')
        self.assertEqual(response, '10000.0')

    def test_buy(self):
        vadim = user("Vadim")
        vadim.buy('BTC', 'USD', 0.1)
        self.assertEqual(vadim.get_balance()['BTC'], 0.1)
        self.assertLess(vadim.get_balance()['USD'], 10000)

if __name__ == "__main__":
    unittest.main()