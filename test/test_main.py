"""This script is used to test the function in main.py"""

import unittest
import os
import requests # pylint: disable=import-error
# from src.main import Main
# import mysql.connector as mysql

HOST = os.environ["HVAC_HOST"]

class TestStringMethods(unittest.TestCase):
    """Test class for the Main class"""
    def test_simulator_up(self):
        """Function to test if we receive an information from the server"""
        request = requests.get(f"{HOST}/api/health")
        self.assertEqual("All system operational Commander!", request.text)

if __name__ == '__main__':
    unittest.main()
