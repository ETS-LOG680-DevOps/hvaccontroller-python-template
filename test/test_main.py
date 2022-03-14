import unittest
import sys
import requests
import json
import os
from src.main import Main
import mysql.connector as mysql

HOST = os.getenv("HVAC_HOST", "http://178.128.234.252:32775")


class TestStringMethods(unittest.TestCase):
    def test_simulator_up(self):
        r = requests.get(f"{HOST}/api/health")
        self.assertEqual("All system operational Commander !", r.text)


if __name__ == "__main__":
    unittest.main()
