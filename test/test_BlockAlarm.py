import unittest
import pygame
from logging import Logger
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockAlarm import BlockAlarm
from exceptions import ExceptionNotFound

SECTION_NAME = "AlarmBlock"

class Test_BlockAlarm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockAlarm(self):
        config = Setting()
        with self.assertRaises(TypeError): BlockAlarm(None, None)
        with self.assertRaises(TypeError): BlockAlarm(None, config)
        with self.assertRaises(TypeError): BlockAlarm(self.logger, None)
        block = BlockAlarm(self.logger, config)
        self.assertIsNotNone(block, "BlockAlarm")
        self.assertIsInstance(block, BlockBase, "BlockBase")

        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
