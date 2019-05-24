import unittest
import pygame
from logging import Logger
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockYandexWeather import BlockYandexWeather

SECTION_NAME = "YandexWeatherBlock"

class Test_BlockYandexWeather(unittest.TestCase):

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

    def test_BlockYandexWeather(self):
        config = Setting()
        with self.assertRaises(TypeError): BlockYandexWeather(None, None)
        with self.assertRaises(TypeError): BlockYandexWeather(None, config)
        with self.assertRaises(TypeError): BlockYandexWeather(self.logger, None)
        block = BlockYandexWeather(self.logger, config)
        self.assertIsNotNone(block, "BlockYandexWeather")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
