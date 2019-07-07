import unittest
from logging import Logger
from exceptions import ExceptionNotFound
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockVoice import BlockVoice

SECTION_NAME = "VoiceBlock"

class Test_Block_Voice(unittest.TestCase):

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


    def test_block_voice(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockVoice(None, None)
        with self.assertRaises(TypeError):
            BlockVoice(None, config)
        with self.assertRaises(TypeError):
            BlockVoice(self.logger, None)
        block = BlockVoice(self.logger, config)
        self.assertIsNotNone(block, "BlockVoice")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

    def test_init_speaker(self):
        config = self._get_setting("")
        block = BlockVoice(self.logger, config)
        self.assertTrue(block is not None, "BlockVoice")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "Speaker", "Speaker")

    def test_init_key(self):
        config = self._get_setting("Speaker")
        block = BlockVoice(self.logger, config)
        self.assertTrue(block is not None, "BlockVoice")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "Key", "Key")

    def test_init_blocks(self):
        config = self._get_setting("Key")
        block = BlockVoice(self.logger, config)
        self.assertTrue(block is not None, "BlockVoice")
        with self.assertRaises(ExceptionNotFound) as err_not_found:
            block.init({})
        self.assertEqual(err_not_found.exception.config_name, SECTION_NAME, SECTION_NAME)
        self.assertEqual(err_not_found.exception.param_name, "BlockList", "BlockList")

    def test_init(self):
        config = self._get_setting(None)
        block = BlockVoice(self.logger, config)
        self.assertTrue(block is not None, "BlockVoice")
        block.init({"Voice": block})
        self.assertIsNotNone(block._speaker, "_speaker")
        self.assertIsNotNone(block._key, "_key")
        self.assertIsNotNone(block._speed, "_speed")
        self.assertIsNotNone(block._blocks, "_blocks")
        self.assertIn(block, block._blocks, "_blocks")
        self.assertEqual(len(block._blocks), 1, "_blocks")

    def _get_setting(self, name):
        params = {
            "Speaker": "omazh",
            "Key": "b55d97e9-6c66-4e1b-966f-c2a6aa9d939d",
            "BlockList": "Voice",
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
