import sys
import time
import threading
from exceptions import ExceptionFormat, ExceptionNotFound
import usb.core
import usb.util
import pygame
import pygame.locals
from modules.BlockSecondBase import BlockSecondBase


class BlockMT8057(BlockSecondBase):
    """description of class"""
    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockMT8057, self).__init__(logger, setting)
        self._warn_zone = None
        self._crit_zone = None
        self._warn_color = (255, 127, 0)
        self._crit_color = (255, 63, 63)
        self._co2_font = None
        self._temp_font = None
        self._co2_pos = None
        self._temp_pos = None
        self._value_co2 = 0
        self._value_temp = 0.0
        self._text_co2 = ""
        self._text_temp = ""

        if sys.platform == "linux":  # Only for Raspberry Pi
            self._t_mt8057 = None

    def init(self, mod_list):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["MT8057Block"]

        self._warn_zone = section.getint("Warn")
        self._crit_zone = section.getint("Crit")
        self._warn_color = self._get_tuple(section.get("WarnColor"))
        self._crit_color = self._get_tuple(section.get("CritColor"))

        co2_font_size = section.getint("CO2FontSize")
        co2_font_name = section.get("CO2FontName")
        co2_is_bold = section.getboolean("CO2FontBold")
        co2_is_italic = section.getboolean("CO2FontItalic")

        temp_font_size = section.getint("TempFontSize")
        temp_font_name = section.get("TempFontName")
        temp_is_bold = section.getboolean("TempFontBold")
        temp_is_italic = section.getboolean("TempFontItalic")

        self._co2_pos = self._get_tuple(section.get("CO2Pos"))
        self._temp_pos = self._get_tuple(section.get("TempPos"))

        if self._warn_zone is None:
            raise ExceptionNotFound(section.name, "Warn")
        if self._crit_zone is None:
            raise ExceptionNotFound(section.name, "Crit")
        if self._warn_color is None:
            raise ExceptionNotFound(section.name, "WarnColor")
        if self._crit_color is None:
            raise ExceptionNotFound(section.name, "CritColor")
        if co2_font_size is None:
            raise ExceptionNotFound(section.name, "CO2FontSize")
        if co2_font_name is None:
            raise ExceptionNotFound(section.name, "CO2FontName")
        if co2_is_bold is None:
            raise ExceptionNotFound(section.name, "CO2FontBold")
        if co2_is_italic is None:
            raise ExceptionNotFound(section.name, "CO2FontItalic")
        if temp_font_size is None:
            raise ExceptionNotFound(section.name, "TempFontSize")
        if temp_font_name is None:
            raise ExceptionNotFound(section.name, "TempFontName")
        if temp_is_bold is None:
            raise ExceptionNotFound(section.name, "TempFontBold")
        if temp_is_italic is None:
            raise ExceptionNotFound(section.name, "TempFontItalic")
        if self._co2_pos is None:
            raise ExceptionNotFound(section.name, "CO2Pos")
        if self._temp_pos is None:
            raise ExceptionNotFound(section.name, "TempPos")

        if len(self._warn_color) != 3:
            raise ExceptionFormat(section.name, "WarnColor")
        if len(self._crit_color) != 3:
            raise ExceptionFormat(section.name, "CritColor")
        if len(self._co2_pos) != 2:
            raise ExceptionFormat(section.name, "CO2Pos")
        if len(self._temp_pos) != 2:
            raise ExceptionFormat(section.name, "TempPos")

        self._co2_font = pygame.font.SysFont(co2_font_name, co2_font_size, co2_is_bold, co2_is_italic)
        self._temp_font = pygame.font.SysFont(temp_font_name, temp_font_size, temp_is_bold, temp_is_italic)
        if sys.platform == "linux":  # Only for Raspberry Pi
            self._t_mt8057 = MT8057(self._logger)
            self._t_mt8057.start()

        self.update_info(True)
        self.set_time(2)

    def update_info(self, is_online):
        if sys.platform == "linux":  # Only for Raspberry Pi
            (self._value_co2, self._value_temp) = self._t_mt8057.get_data()
        else:
            self._value_co2 += 10
            self._value_temp += 0.1
        self._text_co2 = "Концентрация CO2: {0}".format(self._value_co2)
        self._text_temp = "Температура: {0:+.1f}°".format(self._value_temp)
        self._text = "Концентрация CO2: {0}.Температура: {1:+.1f}.".format(self._value_co2, self._value_temp)

    def update_display(self, is_online, screen, size, fore_color, back_color, current_time):
        try:
            if not is_online:
                return

            color = fore_color
            if self._value_co2 >= self._warn_zone:
                color = self._warn_color
            if self._value_co2 >= self._crit_zone:
                color = self._crit_color

            text_size = self._co2_font.size(self._text_co2)
            text_x = (size[0] - text_size[0]) >> 1
            text_y = self._co2_pos[1]
            surf = self._co2_font.render(self._text_co2, True, color, back_color)
            screen.blit(surf, (text_x, text_y))
            # print(text_x)

            text_size = self._co2_font.size(self._text_temp)
            text_x = (size[0] - text_size[0]) >> 1
            text_y = self._temp_pos[1]
            surf = self._temp_font.render(self._text_temp, True, fore_color, back_color)
            screen.blit(surf, (text_x, text_y))
            # print(text_x)
        except Exception as ex:
            self._logger.exception(ex)

    def done(self):
        if sys.platform == "linux":  # Only for Raspberry Pi
            self._t_mt8057.stop()
            self._t_mt8057.join()


class MT8057(threading.Thread):
    VID = 0x04d9
    PID = 0xa052
    RW_TIMEOUT = 0
    REQUEST_TYPE_SEND = usb.util.build_request_type(
        usb.util.CTRL_OUT,
        usb.util.CTRL_TYPE_CLASS,
        usb.util.CTRL_RECIPIENT_INTERFACE)
    REQ_HID_SET_REPORT = 0x09
    HID_REPORT_TYPE_FEATURE = 0x03 << 8

    magic_buf = [0xc4, 0xc6, 0xc0, 0x92, 0x40, 0x23, 0xdc, 0x96]
    ctmp = [0x84, 0x47, 0x56, 0xd6, 0x07, 0x93, 0x93, 0x56]

    def __init__(self, logger):
        threading.Thread.__init__(self, name="mt")
        self._logger = logger
        self._event_stop = threading.Event()
        self._lock = threading.Lock()
        self._temperature = 0.0
        self._concentration = 0
        self._is_init = False
        self._had_driver = False
        self._dev = None
        self._ep = None

    def stop(self):
        self._event_stop.set()

    def run(self):
        self._event_stop.clear()
        while not self._event_stop.is_set():
            try:
                if self._check_init():
                    data = self._dev.read(self._ep, 8, self.RW_TIMEOUT)
                    self._parse(data)
                else:
                    time.sleep(100)
            except Exception as ex:
                self._logger.exception(ex)
                self._release()
                time.sleep(100)
        self._release()

    def get_data(self):
        self._lock.acquire()
        value = (self._concentration, self._temperature)
        self._lock.release()
        return value

    def _decode(self, data):
        shuffle = [2, 4, 0, 7, 1, 6, 5, 3]
        phase1 = []
        phase2 = []
        phase3 = []
        result = []

        for i in range(8):
            phase1.append(data[shuffle[i]])
            phase2.append(phase1[i] ^ self.magic_buf[i])
        for i in range(8):
            phase3.append(((phase2[i] >> 3) | (phase2[(i - 1 + 8) % 8] << 5)) & 0xff)
            result.append((0x100 + phase3[i] - self.ctmp[i]) & 0xff)

        return result

    def _parse(self, data):
        item = self._decode(data)
        r0 = item[0]
        r1 = item[1]
        r2 = item[2]
        r3 = item[3]
        checksum = (r0 + r1 + r2) & 0xff
        if (checksum == r3 and item[4] == 0x0d):
            w = (r1 << 8) + r2
            if r0 == 0x42:  # Ambient Temperature
                w = w * 0.0625 - 273.15
                self._lock.acquire()
                self._temperature = w
                self._lock.release()
            elif r0 == 0x50:  # Relative Concentration of CO2
                self._lock.acquire()
                self._concentration = w
                self._lock.release()
            else:
                pass

    def _check_init(self):
        if self._is_init:
            return True

        self._dev = usb.core.find(idVendor=self.VID, idProduct=self.PID)
        if self._dev is None:
            self._logger.exception("Device not found")
            return False

        self._had_driver = False
        if self._dev.is_kernel_driver_active(0):
            self._dev.detach_kernel_driver(0)
            self._had_driver = True

        self._dev.set_configuration()
        # print(self._dev)
        self._ep = self._dev[0][(0, 0)][0]

        self._dev.ctrl_transfer(
            self.REQUEST_TYPE_SEND,
            self.REQ_HID_SET_REPORT,
            self.HID_REPORT_TYPE_FEATURE,
            0x00, self.magic_buf,
            self.RW_TIMEOUT)
        self._is_init = True
        return True

    def _release(self):
        if not self._is_init:
            return
        try:
            usb.util.release_interface(self._dev, 0)
            if self._had_driver:
                self._dev.attach_kernel_driver(0)
        except Exception as ex:
            self._logger.exception(ex)
            time.sleep(100)
        self._dev = None
        self._had_driver = False
        self._is_init = False
