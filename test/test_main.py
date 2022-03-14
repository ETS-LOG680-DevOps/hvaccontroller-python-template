from pickle import NONE
import unittest
from unittest.mock import patch
import requests
import os
from src.main import Main

HOST = "http://178.128.234.252:32775"
HVAC_TOKEN = "WBhinj3isJ"
MIN_TEMP = "20"
MAX_TEMP = "80"
NB_TICK = "6"
all_env_vars = {"HVAC_HOST": HOST, "HVAC_TOKEN": HVAC_TOKEN, "MIN_TEMP": MIN_TEMP, "MAX_TEMP": MAX_TEMP, "NB_TICK": NB_TICK}


class TestStringMethods(unittest.TestCase):
    def test_simulator_up(self):
        r = requests.get(f"{HOST}/api/health")
        self.assertEqual("All system operational Commander !", r.text)

    @patch.dict(os.environ, all_env_vars, clear=True)
    def test_all_env_variable_exist(self):
        main = Main()
        self.assertEqual(main.HOST, HOST)
        self.assertEqual(main.HVAC_TOKEN, HVAC_TOKEN)
        self.assertEqual(main.MIN_TEMP, float(MIN_TEMP))
        self.assertEqual(main.MAX_TEMP, float(MAX_TEMP))
        self.assertEqual(main.NB_TICK, int(NB_TICK))

    @patch.dict(os.environ, {}, clear=True)
    def test_app_exit_with_empty_token(self):
        with self.assertRaises(SystemExit) as cm:
            main = Main()

        self.assertEqual(cm.exception.code, "Error: Missing environment variable 'HVAC_TOKEN'")

    @patch.dict(os.environ, {"HVAC_TOKEN": HVAC_TOKEN}, clear=True)
    def test_app_run_with_only_token(self):
        main = Main()
        self.assertEqual(main.HOST, HOST)
        self.assertEqual(main.HVAC_TOKEN, HVAC_TOKEN)
        self.assertEqual(main.MIN_TEMP, float(MIN_TEMP))
        self.assertEqual(main.MAX_TEMP, float(MAX_TEMP))
        self.assertEqual(main.NB_TICK, int(NB_TICK))

if __name__ == "__main__":
    unittest.main()
