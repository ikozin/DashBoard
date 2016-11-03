import configparser
import pygame
import pygame.locals
import sys
import threading
import usb.core
import usb.util
from datetime import time
from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockSecondBase import BlockSecondBase


class BlockMT8057(BlockSecondBase):
	"""description of class"""
	def __init__(self, logger, setting):
		"""Initializes (declare internal variables)"""
		super(BlockMT8057, self).__init__(logger, setting)
		self._warnZone = None
		self._critZone = None
		self._warnColor = (255, 127, 0)
		self._critColor = (255, 63, 63)
		self._co2Font = None
		self._tempFont = None
		self._co2Pos = None
		self._tempPos = None
		self._valueCO2 = None
		self._valueTemp = None
		if sys.platform == "linux": # Only for Raspberry Pi
			self._t_mt8057 = None


	def init(self, fileName, isOnline, modList):
		"""Initializes (initialize internal variables)"""
		config = configparser.ConfigParser()
		config.read(fileName, "utf-8")

		section = config["MT8057Block"]
		if section is None: return

		self._warnZone = section.getint("Warn")
		self._critZone = section.getint("Crit")
		self._warnColor = self._getTuple(section.get("WarnColor"))
		self._critColor = self._getTuple(section.get("CritColor"))

		co2FontSize = section.getint("CO2FontSize")
		co2FontName = section.get("CO2FontName")
		co2IsBold = section.getboolean("CO2FontBold")
		co2IsItalic = section.getboolean("CO2FontItalic")

		tempFontSize = section.getint("TempFontSize")
		tempFontName = section.get("TempFontName")
		tempIsBold = section.getboolean("TempFontBold")
		tempIsItalic = section.getboolean("TempFontItalic")

		self._co2Pos = self._getTuple(section.get("CO2Pos"))
		self._tempPos = self._getTuple(section.get("TempPos"))

		if self._warnZone is None:  raise ExceptionNotFound(section.name, "Warn")
		if self._critZone is None:  raise ExceptionNotFound(section.name, "Crit")
		if self._warnColor is None: raise ExceptionNotFound(section.name, "WarnColor")
		if self._critColor is None: raise ExceptionNotFound(section.name, "CritColor")
		if co2FontSize is None:     raise ExceptionNotFound(section.name, "CO2FontSize")
		if co2FontName is None:     raise ExceptionNotFound(section.name, "CO2FontName")
		if co2IsBold   is None:     raise ExceptionNotFound(section.name, "CO2FontBold")
		if co2IsItalic is None:     raise ExceptionNotFound(section.name, "CO2FontItalic")
		if tempFontSize is None:    raise ExceptionNotFound(section.name, "TempFontSize")
		if tempFontName is None:    raise ExceptionNotFound(section.name, "TempFontName")
		if tempIsBold   is None:    raise ExceptionNotFound(section.name, "TempFontBold")
		if tempIsItalic is None:    raise ExceptionNotFound(section.name, "TempFontItalic")
		if self._co2Pos is None:    raise ExceptionNotFound(section.name, "CO2Pos")
		if self._tempPos is None:   raise ExceptionNotFound(section.name, "TempPos")

		if len(self._warnColor) != 3: raise ExceptionFormat(section.name, "WarnColor")
		if len(self._critColor) != 3: raise ExceptionFormat(section.name, "CritColor")
		if len(self._co2Pos) != 2:    raise ExceptionFormat(section.name, "CO2Pos")
		if len(self._tempPos) != 2:   raise ExceptionFormat(section.name, "TempPos")

		self._co2Font = pygame.font.SysFont(co2FontName, co2FontSize, co2IsBold, co2IsItalic)
		self._tempFont = pygame.font.SysFont(tempFontName, tempFontSize, tempIsBold, tempIsItalic)
		if sys.platform == "linux": # Only for Raspberry Pi
			self._t_mt8057 = mt8057()
			self._t_mt8057.start()

		self.updateInfo(isOnline)
		self.setTime(2)


	def updateInfo(self, isOnline):
		if sys.platform == "linux": # Only for Raspberry Pi
			(self._valueCO2, self._valueTemp) = self._t_mt8057.get_data()
		else:
			if (self._valueCO2 is None): self._valueCO2   = 500
			if (self._valueTemp is None): self._valueTemp = 24.970001
			self._valueCO2 += 10
			self._valueTemp += 0.1


	def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
		try:
			if not isOnline: return
			#print("CO2", self._valueCO2, "temp", "{:.1f}".format(self._valueTemp))
			textCO2 = "Концентрация CO2: {0}".format(self._valueCO2)
			textTemp = "Температура: {0:+.1f}°".format(self._valueTemp)

			color = foreColor
			if self._valueCO2 >= self._warnZone:
				color = self._warnColor
			if self._valueCO2 >= self._critZone:
				color = self._critColor
			sz = self._co2Font.size(textCO2)
			x = (size[0] - sz[0]) >> 1
			y = self._co2Pos[1]
			surf = self._co2Font.render(textCO2, True, color, backColor)
			screen.blit(surf, (x, y))
			#print(x)

			sz = self._co2Font.size(textTemp)
			x = (size[0] - sz[0]) >> 1
			y = self._tempPos[1]
			surf = self._tempFont.render(textTemp, True, foreColor, backColor)
			screen.blit(surf, (x, y))
			#print(x)
		except Exception as ex:
			self._logger.exception(ex)


	def done(self):
		""" """
		if sys.platform == "linux": # Only for Raspberry Pi
			self._t_mt8057.stop()
			self._t_mt8057.join()




class mt8057(threading.Thread):
	VID = 0x04d9
	PID = 0xa052
	RW_TIMEOUT = 5000
	REQUEST_TYPE_SEND = usb.util.build_request_type(usb.util.CTRL_OUT, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE)
	REQ_HID_SET_REPORT = 0x09
	HID_REPORT_TYPE_FEATURE = 0x03 << 8

	magic_buf = [0xc4, 0xc6, 0xc0, 0x92, 0x40, 0x23, 0xdc, 0x96]
	ctmp    = [0x84, 0x47, 0x56, 0xd6, 0x07, 0x93, 0x93, 0x56]

	def __init__(self):
		threading.Thread.__init__(self, name="mt")
		self._event_stop = False #threading.Event()
		#self._lock = threading.Lock()
		self._temperature  = None
		self._concentration = None
		self._had_driver = False
		self._dev = usb.core.find(idVendor=self.VID, idProduct=self.PID)

		if self._dev is None:
			raise ValueError("Device not found")

		if self._dev.is_kernel_driver_active(0):
			self._dev.detach_kernel_driver(0)
			self._had_driver = True

		self._dev.set_configuration()
		#print(self._dev)
		self._ep = self._dev[0][(0,0)][0]


	def stop(self):
		self._event_stop = True #.set()


	def run(self):
		self._dev.ctrl_transfer(self.REQUEST_TYPE_SEND, self.REQ_HID_SET_REPORT, self.HID_REPORT_TYPE_FEATURE, 0x00, self.magic_buf, self.RW_TIMEOUT)
		while not self._event_stop: #.is_set():
			data = self._read()
			#print(data)
			self._parse(data)
			time.sleep(0.1)
		self._release()


	def get_data(self):
		#self._lock.acquire()
		value = (self._concentration, self._temperature)
		#self._lock.release()
		return value


	def _read(self):
		return self._dev.read(self._ep, 8, self.RW_TIMEOUT)


	def _decode(self, data):
		shuffle = [2, 4, 0, 7, 1, 6, 5, 3]
		phase1  = []
		phase2  = []
		phase3  = []
		result  = []

		for i in range(8):
			phase1.append(data[shuffle[i]])
			phase2.append(phase1[i] ^ self.magic_buf[i])
		for i in range(8):
			phase3.append(((phase2[i] >> 3) | (phase2[ (i-1+8)%8 ] << 5) ) & 0xff)
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
			if (r0 == 0x42): # Ambient Temperature
				w = w * 0.0625 - 273.15
				#self._lock.acquire()
				self._temperature  = w
				#self._lock.release()
			elif (r0 == 0x50): # Relative Concentration of CO2
				#self._lock.acquire()
				self._concentration = w
				#self._lock.release()
			else:
				pass

	def _release(self):
		usb.util.release_interface(self._dev, 0)
		if self._had_driver:
			self._dev.attach_kernel_driver(0)
