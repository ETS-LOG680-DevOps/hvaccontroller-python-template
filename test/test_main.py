import unittest
import sys
import requests
import json
import os
from src.main import Main
# import mysql.connector as mysql

HOST = os.environ["HVAC_HOST"]
TOKEN = "89103df59ad0cda23c2f"
TICKS = "6"
HOT_LIMIT = "80"
COLD_LIMIT = "20"

class TestStringMethods(unittest.TestCase):

    def test_simulator_up(self):
        r = requests.get(f"{HOST}/api/health") 
        self.assertEqual("All system operational Commander !", r.text)
    
    def test_token(self):
        hvac = Main()
        self.assertEqual(TOKEN, hvac.TOKEN)
    
    def test_hot_limit(self):
        hvac = Main()
        self.assertNotEqual(HOT_LIMIT, hvac.HOT_LIMIT)


    def test_cold_limit(self):
        hvac = Main()
        self.assertNotEqual(COLD_LIMIT, hvac.COLD_LIMIT)

    def test_ticks(self):
        hvac = Main()
        self.assertNotEqual(TICKS, hvac.TICKS)
    
if __name__ == '__main__':
    unittest.main()
