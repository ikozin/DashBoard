import unittest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockIR import BlockIR

SECTION_NAME = "IRBlock"

class Test_Block_IR(unittest.TestCase):

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

    def test_block_ir(self):
        config = Setting()
        with self.assertRaises(TypeError): BlockIR(None, None)
        with self.assertRaises(TypeError): BlockIR(None, config)
        with self.assertRaises(TypeError): BlockIR(self.logger, None)
        block = BlockIR(self.logger, config)
        self.assertIsNotNone(block, "BlockIR")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
