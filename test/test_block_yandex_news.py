import unittest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_yandex_news import BlockYandexNews

SECTION_NAME = "YandexNewsBlock"

class TestBlockYandexNews(unittest.TestCase):

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

    def test_block_yandex_news(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockYandexNews(None, None)
        with self.assertRaises(TypeError):
            BlockYandexNews(None, config)
        with self.assertRaises(TypeError):
            BlockYandexNews(self.logger, None)
        block = BlockYandexNews(self.logger, config)
        self.assertIsNotNone(block, "BlockYandexNews")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

if __name__ == '__main__':
    unittest.main()
