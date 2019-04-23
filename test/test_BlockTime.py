import unittest
from logging import Logger
from setting import Setting
from modules.BlockTime import BlockTime
from exceptions import ExceptionNotFound

SECTION_NAME = "TimeBlock"

class Test_BlockTime(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockTime(self):
        config = Setting()

        with self.assertRaises(TypeError): BlockTime(None, None)
        with self.assertRaises(TypeError): BlockTime(None, config)
        with self.assertRaises(TypeError): BlockTime(self.logger, None)

        block = BlockTime(self.logger, config)
        self.assertIsNotNone(block, "BlockTime")

    def test_Init_creator(self):
        config = Setting()

        with self.assertRaises(TypeError): BlockTime(None, None)
        with self.assertRaises(TypeError): BlockTime(None, config)
        with self.assertRaises(TypeError): BlockTime(self.logger, None)
        
        block = BlockTime(self.logger, config)
        self.assertIsNotNone(block, "BlockTime")
        with self.assertRaises(KeyError):
            block.init({})

    def test_Init_FontName(self):
        config = self._getSetting("")
        
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "FontName", "FontName")
    
    def test_Init_FontSize(self):
        config = self._getSetting("FontName")
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "FontSize", "FontSize")
    
    def test_Init_FontBold(self):
        config = self._getSetting("FontSize")
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "FontBold", "FontBold")

    def test_Init_FontItalic(self):
        config = self._getSetting("FontBold")
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "FontItalic", "FontItalic")
    
    def test_Init_finalize(self):
        config = self._getSetting(None)
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(BaseException) as ErrFont:
            block.init({})
        self.assertEqual(ErrFont.exception.__str__(), "font not initialized", "Font")


    def _getSetting(self, name):
        params = {
            "FontName": "Helvetica",
            "FontSize": 384,
            "FontBold": True,
            "FontItalic": False,
        }
        config = Setting()
        config.Configuration.add_section(SECTION_NAME)
        if name == "":
            return config
        section = config.Configuration[SECTION_NAME]
        for key, value in params.items():
            section[key] = value.__str__()
            if key == name:
                break
        return config

if __name__ == '__main__':
    unittest.main()
