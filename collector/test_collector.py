import unittest
import requests
import mysql.connector
from unittest.mock import MagicMock

import lambda_function

EXTERNAL_API_RESPONSE = {
  "result": {
    "market:binance-us:1inchusd": 0.612,
    "market:binance-us:1inchusdt": 0.607,
    "market:binance-us:aaveusd": 78.1,
    "market:binance-us:aaveusdt": 78.01,
    "market:binance-us:achusd": 0.0119,
    "market:binance-us:achusdt": 0.01192
  },
  "cursor": {
    "last": "4iYvqiSe0AxATF0Q_D_vgYVAIj3wLO-1Rev6gdwvyg6TA8FsgasrI0ge86YDGg",
    "hasMore": "false"
  },
  "allowance": {
    "cost": 0.015,
    "remaining": 9.901,
    "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
  }
}

class MockCursor():
    _affected_rows = 1
    def execute(query):
        return True

class MockDB():
    def cursor():
        return MockCursor
    def commit():
        return True

class TestCollector(unittest.TestCase):
    def setUp(self) -> None:
        requests.get = MagicMock(return_value = EXTERNAL_API_RESPONSE)
        mysql.connector.connect = MagicMock(return_value = MockDB)
        
        return super().setUp()

    def test_get_market_prices(self):
        response = lambda_function.get_market_prices()
        self.assertEqual(response, EXTERNAL_API_RESPONSE)

    def test_save_results(self):        
        response = lambda_function.save_results(EXTERNAL_API_RESPONSE['result'])
        self.assertEqual(response.get('affected_rows'),1)
        self.assertIn('insert_duration',response)


    def test_build_query(self):
        lambda_function.process_result = MagicMock(return_value = {
            'exchange': 'exchange',
            'pair': 'pair',
            'price': 1
        })
        response = lambda_function.build_query(EXTERNAL_API_RESPONSE['result'])
        lambda_function.process_result.assert_called()
        self.assertEqual(response.count('''('exchange', 'pair', 1'''), len(EXTERNAL_API_RESPONSE['result']))

    def test_process_result(self):
        response = lambda_function.process_result('market:binance-us:1inchusd', 0.1)
        self.assertIn('exchange', response)
        self.assertIn('pair', response)
        self.assertIn('price', response)

if __name__ == '__main__':
    unittest.main()