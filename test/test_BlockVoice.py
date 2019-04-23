import unittest
import pygame
from logging import Logger
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockVoice import BlockVoice
from exceptions import ExceptionNotFound

SECTION_NAME = "VoiceBlock"

class Test_BlockVoice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockVoice(self):
        config = Setting()

        with self.assertRaises(TypeError): BlockVoice(None, None)
        with self.assertRaises(TypeError): BlockVoice(None, config)
        with self.assertRaises(TypeError): BlockVoice(self.logger, None)

        block = BlockVoice(self.logger, config)
        self.assertIsNotNone(block, "BlockVoice")
        self.assertIsInstance(block, BlockBase, "BlockBase")

        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
