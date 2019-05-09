import unittest
import pygame
from logging import Logger
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockWatcher import BlockWatcher
from exceptions import ExceptionNotFound

SECTION_NAME = "WatcherBlock"

class Test_BlockWatcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.font.init()
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockWatcher(self):
        config = Setting()
        with self.assertRaises(TypeError): BlockWatcher(None, None)
        with self.assertRaises(TypeError): BlockWatcher(None, config)
        with self.assertRaises(TypeError): BlockWatcher(self.logger, None)
        block = BlockWatcher(self.logger, config)
        self.assertIsNotNone(block, "BlockWatcher")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
