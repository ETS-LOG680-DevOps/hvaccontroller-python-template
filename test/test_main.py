"""This script is used to test the function in main.py"""

import unittest
import os
import requests
from src.main import Main
# import mysql.connector as mysql

HOST = os.environ["HVAC_HOST"]
TOKEN = "89103df59ad0cda23c2f"
TICKS = "6"
HOT_LIMIT = "80"
COLD_LIMIT = "20"

class TestStringMethods(unittest.TestCase):
    """Test class for the Main class"""
    def test_simulator_up(self):
        """Function to test if we receive an information from the server"""
        request = requests.get(f"{HOST}/api/health")
        self.assertEqual("All system operational Commander !", request.text)

    def test_token(self):
        """Test if the token in the environment variable is good"""
        hvac = Main()
        self.assertEqual(TOKEN, hvac.token)

    def test_hot_limit(self):
        """Test if the hot limit is different from the default value"""
        hvac = Main()
        self.assertNotEqual(HOT_LIMIT, hvac.hot_limit)


    def test_cold_limit(self):
        """Test if the cold limit is different from the default value"""
        hvac = Main()
        self.assertNotEqual(COLD_LIMIT, hvac.cold_limit)

    def test_ticks(self):
        """Test if the number of ticks is different from the default value"""
        hvac = Main()
        self.assertNotEqual(TICKS, hvac.ticks)

if __name__ == '__main__':
    unittest.main()
