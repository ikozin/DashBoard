import unittest
from logging import Logger
import pygame
from .setting import Setting
from modules.BlockBase import BlockBase
from modules.block_alarm import BlockAlarm

SECTION_NAME = "AlarmBlock"

class TestBlockAlarm(unittest.TestCase):

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

    def test_block_alarm(self):
        config = Setting()
        with self.assertRaises(TypeError):
            BlockAlarm(None, None)
        with self.assertRaises(TypeError):
            BlockAlarm(None, config)
        with self.assertRaises(TypeError):
            BlockAlarm(self.logger, None)
        block = BlockAlarm(self.logger, config)
        self.assertIsNotNone(block, "BlockAlarm")
        self.assertIsInstance(block, BlockBase, "BlockBase")

        with self.assertRaises(KeyError):
            block.init({})

    def test_init(self):
        config = self._get_setting(None)
        block = BlockAlarm(self.logger, config)
        self.assertTrue(block is not None, "BlockAlarm")
        block.init({})
        self.assertIsNotNone(block._blocks, "_blocks")
        self.assertIsNotNone(block._alarm_block, "_alarm_block")
        self.assertIsNotNone(block._functions, "_functions")

    def _get_setting(self, name):
        params = {
            "BlockList": "Time",
            "List": "",
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
