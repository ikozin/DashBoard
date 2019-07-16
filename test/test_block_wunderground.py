import unittest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_wunderground import BlockWunderGround

SECTION_NAME = "WunderGroundBlock"

class TestBlockWunderGround(unittest.TestCase):

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

    def test_block_wunderground(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockWunderGround(None, None)
        with self.assertRaises(TypeError):
            BlockWunderGround(None, config)
        with self.assertRaises(TypeError):
            BlockWunderGround(self.logger, None)
        block = BlockWunderGround(self.logger, config)
        self.assertIsNotNone(block, "BlockWunderGround")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
