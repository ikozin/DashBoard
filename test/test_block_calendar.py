import unittest
from logging import Logger
from .exceptions import ExceptionNotFound
import pygame
from .setting import Setting
from .modules.BlockBase import BlockBase
from .modules.block_calendar import BlockCalendar

SECTION_NAME = "CalendarBlock"

class TestBlockCalendar(unittest.TestCase):

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

    def test_block_calendar(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockCalendar(None, None)
        with self.assertRaises(TypeError):
            BlockCalendar(None, config)
        with self.assertRaises(TypeError):
            BlockCalendar(self.logger, None)
        block = BlockCalendar(self.logger, config)
        self.assertIsNotNone(block, "BlockCalendar")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

    def test_init_font_name(self):
        config = self._get_setting("")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "FontName", "FontName")

    def test_init_font_size(self):
        config = self._get_setting("FontName")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "FontSize", "FontSize")

    def test_init_font_bold(self):
        config = self._get_setting("FontSize")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "FontBold", "FontBold")

    def test_init_font_italic(self):
        config = self._get_setting("FontBold")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "FontItalic", "FontItalic")

    def test_init_position(self):
        config = self._get_setting("FontItalic")
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "Position", "Position")

    def test_init(self):
        config = self._get_setting(None)
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        block.init({})
        self.assertIsNotNone(block._days_long, "_days_long")
        self.assertIsNotNone(block._months, "_months")
        self.assertIsNotNone(block._weekday_shot, "_weekday_shot")
        self.assertEqual(len(block._weekday_shot), 7, "_weekday_shot")
        self.assertIsNotNone(block._weekday_long, "_weekday_long")
        self.assertEqual(len(block._weekday_long), 7, "_weekday_long")
        self.assertIsNotNone(block._font, "_font")
        self.assertIsNotNone(block._pos, "_pos")
        self.assertIsNone(block._time, "_time")

    def test_execute(self):
        config = self._get_setting(None)
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        block.init({})
        block.execute()
        self.assertIsNotNone(block._text, "_text")
        self.assertIsNone(block._time, "_time")

    def test_get_text(self):
        config = self._get_setting(None)
        block = BlockCalendar(self.logger, config)
        self.assertTrue(block is not None, "BlockCalendar")
        block.init({})
        text = block.get_text()
        self.assertIsNotNone(text, "text")
        self.assertIsNotNone(block._text, "_text")
        self.assertIsNone(block._time, "_time")

    def _get_setting(self, name):
        params = {
            "FontName": "Helvetica",
            "FontSize": 170,
            "FontBold": True,
            "FontItalic": False,
            "Position": 80
        }
        config = Setting()
        config.configuration.add_section(SECTION_NAME)
        if name == "":
            return config
        section = config.configuration[SECTION_NAME]
        for key, value in params.items():
            section[key] = value.__str__()
            if key == name:
                break
        return config

if __name__ == '__main__':
    unittest.main()
