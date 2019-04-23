import unittest
from logging import Logger
from setting import Setting
from modules.BlockYandexWeather import BlockYandexWeather
from exceptions import ExceptionNotFound

SECTION_NAME = "YandexWeatherBlock"

class Test_BlockYandexWeather(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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

if __name__ == '__main__':
    unittest.main()
