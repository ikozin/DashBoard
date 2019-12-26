import unittest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_swap import BlockSwap

SECTION_NAME = "SwapBlock"


class TestBlockSwap(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.font.init()
        cls.logger = Logger("Log")

    # def setUp(self):
    #    super().setUp()

    # def tearDown(self):
    #    super().tearDown()

    # def tearDownClass(cls):
    #    super().tearDownClass()

    def test_block_swap(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockSwap(None, None)
        with self.assertRaises(TypeError):
            BlockSwap(None, config)
        with self.assertRaises(TypeError):
            BlockSwap(self.logger, None)
        block = BlockSwap(self.logger, config)
        self.assertIsNotNone(block, "BlockSwap")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})


if __name__ == '__main__':
    unittest.main()
