import unittest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_watcher import BlockWatcher

SECTION_NAME = "WatcherBlock"

class TestBlockWatcher(unittest.TestCase):

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

    def test_block_watcher(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockWatcher(None, None)
        with self.assertRaises(TypeError):
            BlockWatcher(None, config)
        with self.assertRaises(TypeError):
            BlockWatcher(self.logger, None)
        block = BlockWatcher(self.logger, config)
        self.assertIsNotNone(block, "BlockWatcher")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
