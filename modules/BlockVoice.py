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
        self._blockSource = None
        self._speaker = None
        self._speed = 1
        self._key = None


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["VoiceBlock"]

        self._speaker = section.get("Speaker")
        self._key = section.get("Key")

        if self._speaker is None: raise ExceptionNotFound(section.name, "Speaker")
        if self._key is None:     raise ExceptionNotFound(section.name, "Key")


    def proccedEvent(self, event, isOnline):
        try:
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_SPACE):
                if self._blockSource:
                    text = self._blockSource.getText()
                    if not text: return
                    soundFile = self.__getvoicetext(text)
                    pygame.mixer.music.load(soundFile)
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play()
                    #if not pygame.mixer.get_busy():
                    #    soundFile = getvoicetext(self._weather_text)
                    #    sound = pygame.mixer.Sound(soundFile)
                    #    sound.set_volume(1.0)   # Now plays at 100% of full volume.
                    #    sound.play()            # Sound plays at full volume by default
        except Exception as ex:
            self._logger.exception(ex)


    def setTextSource(self, block):
        if not isinstance(block, BlockBase):
            raise("Передаваемый параметр должен быть наследником BlockBase")
        self._blockSource = block

    
    def __getvoicetext(self, text):
        fileName = "text.wav";
        url = "https://tts.voicetech.yandex.net/generate?format=wav&lang=ru-RU&speaker={0}&emotion=good&speed={1}&key={2}&text='{3}'".format(self._speaker, self._speed, self._key, parse.quote(text))
        out = open(fileName, "wb")
        out.write(request.urlopen(url).read())
        out.close()
        return fileName
