import unittest
from logging import Logger
from setting import Setting
from modules.BlockSwap import BlockSwap
from exceptions import ExceptionNotFound

SECTION_NAME = "SwapBlock"

class Test_BlockSwap(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockSwap(self):
        config = Setting()

        with self.assertRaises(TypeError): BlockSwap(None, None)
        with self.assertRaises(TypeError): BlockSwap(None, config)
        with self.assertRaises(TypeError): BlockSwap(self.logger, None)

        block = BlockSwap(self.logger, config)
        self.assertIsNotNone(block, "BlockSwap")

if __name__ == '__main__':
    unittest.main()
