import unittest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockOpenWeatherMap import BlockOpenWeatherMap

SECTION_NAME = "OpenWeatherMapBlock"

class Test_Block_Openweathermap(unittest.TestCase):

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

    def test_block_openweathermap(self):
        config = Setting()
        with self.assertRaises(TypeError): BlockOpenWeatherMap(None, None)
        with self.assertRaises(TypeError): BlockOpenWeatherMap(None, config)
        with self.assertRaises(TypeError): BlockOpenWeatherMap(self.logger, None)
        block = BlockOpenWeatherMap(self.logger, config)
        self.assertIsNotNone(block, "BlockOpenWeatherMap")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
