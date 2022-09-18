import unittest
from unittest.mock import MagicMock
import mysql.connector

from lambda_function import lambda_handler

class MockCursor():
    def execute():
        return True

class MockDB():
    def cursor():
        return MockCursor
    def commit():
        return True

class TestCollector(unittest.TestCase):
    def setUp(self) -> None:
        mysql.connector.connect = MagicMock(return_value = MockDB)
        
        return super().setUp()

    def test_get_market_prices(self):
        return


if __name__ == '__main__':
    unittest.main()
        
