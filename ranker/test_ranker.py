import unittest
import mysql.connector
from unittest.mock import MagicMock
from unittest.mock import patch

import lambda_function

PAIR = 'btcusd'
class MockCursor():
    def execute(query):
        return True
    def fetchall():
        return []

class MockDB():
    def cursor(dictionary = True):
        return MockCursor
    def commit():
        return True

class TestRanker(unittest.TestCase):
    def setUp(self) -> None:
        mysql.connector.connect = MagicMock(return_value = MockDB)
        
        return super().setUp()

    def test_get_exchange_pairs(self):
        response = lambda_function.get_exchange_pairs()
        print(response)
        # self.assertEqual(response, [])

    # def test_get_pair_prices(self):
    #     response = lambda_function.get_pair_prices(PAIR)
    #     self.assertEqual(response, [])


if __name__ == '__main__':
    unittest.main()
        
