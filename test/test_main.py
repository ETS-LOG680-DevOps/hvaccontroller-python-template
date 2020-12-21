import unittest
import sys
import requests
import json
import os
from src.main import Main
import mysql.connector as mysql

class TestStringMethods(unittest.TestCase):

    def test_simulator_up(self):
        r = requests.get(f"http://ec2-52-7-99-159.compute-1.amazonaws.com:32775/api/health") 
        self.assertEqual("All system operational Commander !", r.text)
    
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()