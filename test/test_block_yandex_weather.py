import unittest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_yandex_weather import BlockYandexWeather

SECTION_NAME = "YandexWeatherBlock"

class TestBlockYandexWeather(unittest.TestCase):

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

    def test_block_yandex_weather(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockYandexWeather(None, None)
        with self.assertRaises(TypeError):
            BlockYandexWeather(None, config)
        with self.assertRaises(TypeError):
            BlockYandexWeather(self.logger, None)
        block = BlockYandexWeather(self.logger, config)
        self.assertIsNotNone(block, "BlockYandexWeather")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
