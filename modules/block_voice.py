import urllib.request as request
import urllib.parse as parse
import pygame
import pygame.locals

from exceptions import ExceptionNotFound
from modules.BlockBase import BlockBase
from logging import Logger
from setting import Setting

# "Использует сервис "Yandex SpeechKit Cloud" https://tech.yandex.ru/speechkit/cloud/


class BlockVoice(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockVoice, self).__init__(logger, setting)
        self._blocks = []
        self._speaker = None
        self._speed = 1
        self._key = None

    def init(self, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["VoiceBlock"]

        self._speaker = section.get("Speaker")
        self._speed = section.getfloat("Speed")
        self._key = section.get("Key")
        selection = section.get("BlockList", fallback="")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip()]
        for name in selection:
            if name in mod_list:
                self.add_block(mod_list[name])

        if self._speaker is None:
            raise ExceptionNotFound(section.name, "Speaker")
        if self._speed is None:
            raise ExceptionNotFound(section.name, "Speed")
        if self._key is None:
            raise ExceptionNotFound(section.name, "Key")
        if not self._blocks:
            raise ExceptionNotFound(section.name, "BlockList")

        self.update_info(True)

    def procced_event(self, event, is_online):
        try:
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_SPACE):
                self.execute()
        except Exception as ex:
            self._logger.exception(ex)

    def add_block(self, block: BlockBase) -> None:
        if not isinstance(block, BlockBase):
            raise TypeError("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)

    def execute(self, *args) -> None:
        if len(args) == 1:
            text = args[0]
        elif self._blocks:
            text = ". ".join(map(lambda block: block.get_text(), self._blocks))
        if not text:
            return
        sound_file = self.__getvoicetext(text)
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

    def __getvoicetext(self, text):
        filename = "text.wav"
        url = "https://tts.voicetech.yandex.net/generate?" \
            "format=wav&lang=ru-RU&speaker={0}&emotion=good&speed={1}&key={2}&text='{3}'" \
            .format(
                self._speaker,
                self._speed,
                self._key,
                parse.quote(text))
        with open(filename, "wb") as file:
            file.write(request.urlopen(url).read())
        return filename
