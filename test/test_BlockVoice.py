import unittest
import pygame
from logging import Logger
from setting import Setting
from modules.BlockBase import BlockBase
from modules.BlockVoice import BlockVoice
from exceptions import ExceptionNotFound

SECTION_NAME = "VoiceBlock"

class Test_BlockVoice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger("Log")

    #def setUp(self):
    #    super().setUp()

    #def tearDown(self):
    #    super().tearDown()

    #def tearDownClass(cls):    
    #    super().tearDownClass()


    def test_BlockVoice(self):
        config = Setting()
        with self.assertRaises(TypeError): BlockVoice(None, None)
        with self.assertRaises(TypeError): BlockVoice(None, config)
        with self.assertRaises(TypeError): BlockVoice(self.logger, None)
        block = BlockVoice(self.logger, config)
        self.assertIsNotNone(block, "BlockVoice")
        self.assertIsInstance(block, BlockBase, "BlockBase")
        with self.assertRaises(KeyError):
            block.init({})

    def test_Init_Speaker(self):
        config = self._getSetting("")
        block = BlockVoice(self.logger, config)
        self.assertTrue(block is not None, "BlockVoice")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "Speaker", "Speaker")

    def test_Init_Key(self):
        config = self._getSetting("Speaker")
        block = BlockVoice(self.logger, config)
        self.assertTrue(block is not None, "BlockVoice")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "Key", "Key")

    def test_Init_Blocks(self):
        config = self._getSetting("Key")
        block = BlockVoice(self.logger, config)
        self.assertTrue(block is not None, "BlockVoice")
        with self.assertRaises(ExceptionNotFound) as ErrNotFound:
            block.init({})
        self.assertEqual(ErrNotFound.exception.configName, SECTION_NAME, SECTION_NAME)
        self.assertEqual(ErrNotFound.exception.paramName, "BlockList", "BlockList")

    def test_Init_finalize(self):
        config = self._getSetting(None)
        block = BlockVoice(self.logger, config)
        self.assertTrue(block is not None, "BlockVoice")
        block.init({"Voice": block})
        self.assertIsNotNone(block._speaker, "_speaker")
        self.assertIsNotNone(block._key, "_key")
        self.assertIsNotNone(block._speed, "_speed")
        self.assertIsNotNone(block._blocks, "_blocks")
        self.assertIn(block, block._blocks, "_blocks")
        self.assertEqual(len(block._blocks), 1, "_blocks")

    def _getSetting(self, name):
        params = {
            "Speaker": "omazh",
            "Key": "b55d97e9-6c66-4e1b-966f-c2a6aa9d939d",
            "BlockList": "Voice",
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
