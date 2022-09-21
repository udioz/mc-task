import unittest
import requests
import mysql.connector
from unittest.mock import MagicMock

from lambda_function import lambda_handler


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
        from lambda_function import get_market_prices
        response = get_market_prices()
        self.assertEqual(response, EXTERNAL_API_RESPONSE)

    def test_save_results(self):
        from lambda_function import save_results
        response = save_results(EXTERNAL_API_RESPONSE['result'])
        self.assertTrue(response)

    def test_build_query(self):
        import lambda_function        
        lambda_function.process_result = MagicMock(return_value = {
            'exchange': 'exchange',
            'pair': 'pair',
            'price': 1
        })
        response = lambda_function.build_query(EXTERNAL_API_RESPONSE['result'])
        lambda_function.process_result.assert_called()
        self.assertEqual(response.count('''('exchange', 'pair', 1)'''), len(EXTERNAL_API_RESPONSE['result']))

    def test_process_result(self):
        from lambda_function import process_result
        response = process_result('market:binance-us:1inchusd', 0.1)
        print(response)


if __name__ == '__main__':
    unittest.main()
        
