import urllib.request as request
import urllib.parse as parse
import configparser 
import pygame
import pygame.locals

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase

#"Использует сервис "Yandex SpeechKit Cloud" https://tech.yandex.ru/speechkit/cloud/
class BlockVoice(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockVoice, self).__init__(logger, setting)
        self._blocks = []
        self._speaker = None
        self._speed = 1
        self._key = None


    def init(self, fileName, isOnline, modList):
        """Initializes (initialize internal variables)"""
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["VoiceBlock"]

        self._speaker = section.get("Speaker")
        self._key = section.get("Key")
        selection = section.get("BlockList", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip()]
        for name in selection:
            if name in modList:
                self.addBlock(modList[name])

        if self._speaker is None: raise ExceptionNotFound(section.name, "Speaker")
        if self._key is None:     raise ExceptionNotFound(section.name, "Key")
        if not self._blocks:      raise ExceptionNotFound(section.name, "BlockList")

        self.updateInfo(isOnline)


    def proccedEvent(self, event, isOnline):
        try:
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_SPACE):
                if self._blocks:
                    text = ". ".join(map(lambda block: block.getText(), self._blocks))
                    if not text: return
                    soundFile = self.__getvoicetext(text)
                    pygame.mixer.music.load(soundFile)
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play()
        except Exception as ex:
            self._logger.exception(ex)


    def addBlock(self, block):
        """  """
        if not isinstance(block, BlockBase):
            raise("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)

    
    def __getvoicetext(self, text):
        fileName = "text.wav";
        url = "https://tts.voicetech.yandex.net/generate?format=wav&lang=ru-RU&speaker={0}&emotion=good&speed={1}&key={2}&text='{3}'".format(self._speaker, self._speed, self._key, parse.quote(text))
        out = open(fileName, "wb")
        out.write(request.urlopen(url).read())
        out.close()
        return fileName
