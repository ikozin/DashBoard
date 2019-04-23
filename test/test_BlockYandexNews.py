import unittest
from logging import Logger
from setting import Setting
from modules.BlockYandexNews import BlockYandexNews
from exceptions import ExceptionNotFound

SECTION_NAME = "YandexNewsBlock"

class Test_BlockYandexNews(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockYandexNews(self):
        config = Setting()

        with self.assertRaises(TypeError): BlockYandexNews(None, None)
        with self.assertRaises(TypeError): BlockYandexNews(None, config)
        with self.assertRaises(TypeError): BlockYandexNews(self.logger, None)

        block = BlockYandexNews(self.logger, config)
        self.assertIsNotNone(block, "BlockYandexNews")

if __name__ == '__main__':
    unittest.main()