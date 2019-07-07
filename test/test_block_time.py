import unittest
from logging import Logger
from exceptions import ExceptionNotFound
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockTime import BlockTime

SECTION_NAME = "TimeBlock"

class Test_Block_Time(unittest.TestCase):

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

    def test_block_time(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockTime(None, None)
        with self.assertRaises(TypeError):
            BlockTime(None, config)
        with self.assertRaises(TypeError):
            BlockTime(self.logger, None)
        block = BlockTime(self.logger, config)
        self.assertIsNotNone(block, "BlockTime")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

    def test_init_font_name(self):
        config = self._get_setting("")
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "FontName", "FontName")

    def test_init_font_size(self):
        config = self._get_setting("FontName")
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "FontSize", "FontSize")

    def test_init_font_bold(self):
        config = self._get_setting("FontSize")
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "FontBold", "FontBold")

    def test_init_font_italic(self):
        config = self._get_setting("FontBold")
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "FontItalic", "FontItalic")

    def test_init(self):
        config = self._get_setting(None)
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        block.init({})
        self.assertIsNotNone(block._font, "_font")
        self.assertIsNone(block._time, "_time")

    def test_execute(self):
        config = self._get_setting(None)
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        block.init({})
        block.execute()
        self.assertIsNotNone(block._text, "_text")
        self.assertIsNone(block._time, "_time")

    def test_get_text(self):
        config = self._get_setting(None)
        block = BlockTime(self.logger, config)
        self.assertTrue(block is not None, "BlockTime")
        block.init({})
        text = block.get_text()
        self.assertIsNotNone(text, "text")
        self.assertIsNotNone(block._text, "_text")
        self.assertIsNone(block._time, "_time")

    def _get_setting(self, name):
        params = {
            "FontName": "Helvetica",
            "FontSize": 384,
            "FontBold": True,
            "FontItalic": False,
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
