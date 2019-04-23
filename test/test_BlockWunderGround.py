import unittest
from logging import Logger
from setting import Setting
from modules.BlockWunderGround import BlockWunderGround
from exceptions import ExceptionNotFound

SECTION_NAME = "WunderGroundBlock"

class Test_BlockWunderGround(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockWunderGround(self):
        config = Setting()

        with self.assertRaises(TypeError): BlockWunderGround(None, None)
        with self.assertRaises(TypeError): BlockWunderGround(None, config)
        with self.assertRaises(TypeError): BlockWunderGround(self.logger, None)

        block = BlockWunderGround(self.logger, config)
        self.assertIsNotNone(block, "BlockWunderGround")

if __name__ == '__main__':
    unittest.main()

