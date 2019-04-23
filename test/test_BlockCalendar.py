import unittest
import pygame
from logging import Logger
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockCalendar import BlockCalendar
from exceptions import ExceptionNotFound

SECTION_NAME = "CalendarBlock"

class Test_BlockCalendar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockCalendar(self):
        config = Setting()

        with self.assertRaises(TypeError): BlockCalendar(None, None)
        with self.assertRaises(TypeError): BlockCalendar(None, config)
        with self.assertRaises(TypeError): BlockCalendar(self.logger, None)

        block = BlockCalendar(self.logger, config)
        self.assertIsNotNone(block, "BlockCalendar")
        self.assertIsInstance(block, BlockBase, "BlockBase")

        with self.assertRaises(KeyError):
            block.init({})

    def test_Init_FontName(self):
        config = self._getSetting("")
        
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "FontName", "FontName")
    
    def test_Init_FontSize(self):
        config = self._getSetting("FontName")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "FontSize", "FontSize")
    
    def test_Init_FontBold(self):
        config = self._getSetting("FontSize")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "FontBold", "FontBold")

    def test_Init_FontItalic(self):
        config = self._getSetting("FontBold")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "FontItalic", "FontItalic")
    
    def test_Init_Position(self):
        config = self._getSetting("FontItalic")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "Position", "Position")
    
    def test_Init_finalize(self):
        config = self._getSetting(None)
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        pygame.font.init()
        block.init({})
        self.assertIsNotNone(block._font, "_font")
        self.assertIsNotNone(block._pos, "_pos")

    def _getSetting(self, name):
        params = {
            "FontName": "Helvetica",
            "FontSize": 170,
            "FontBold": True,
            "FontItalic": False,
            "Position": 80
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
