import unittest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockMT8057 import BlockMT8057

SECTION_NAME = "MT8057Block"

class Test_Block_MT8057(unittest.TestCase):

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

    def test_block_mt8057(self):
        config = Setting()
        with self.assertRaises(TypeError): BlockMT8057(None, None)
        with self.assertRaises(TypeError): BlockMT8057(None, config)
        with self.assertRaises(TypeError): BlockMT8057(self.logger, None)
        block = BlockMT8057(self.logger, config)
        self.assertIsNotNone(block, "BlockMT8057")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
