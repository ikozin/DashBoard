import datetime
import configparser
import pygame
import pygame.locals
import usb.core

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase


class BlockMT8057(BlockBase):
	"""description of class"""
	VID = 0x04d9
	PID = 0xa052

	magic_buf   = [0xc4, 0xc6, 0xc0, 0x92, 0x40, 0x23, 0xdc, 0x96]
	ctmp        = [0x84, 0x47, 0x56, 0xd6, 0x07, 0x93, 0x93, 0x56]

	def __init__(self, logger, setting):
		"""Initializes (declare internal variables)"""
		super(BlockMT8057, self).__init__(logger, setting)
		self._green = None
		self._yellow = None
		self._had_driver = False
		self._dev = None


	def init(self, fileName, isOnline, modList):
		"""Initializes (initialize internal variables)"""
		# ��������� ���������
		config = configparser.ConfigParser()
		config.read(fileName, "utf-8")

		section = config["MT8057Block"]
		if section is None: return

		self._green = section.getint("Green")
		self._yellow = section.getint("Yellow")

		if self._green is None:  raise ExceptionNotFound(section.name, "Green")
		if self._yellow is None: raise ExceptionNotFound(section.name, "Yellow")

		self._had_driver = False
		self._dev = usb.core.find(idVendor=self.VID, idProduct=self.PID)
		if self._dev is None:   raise ValueError("Device not found")
		if self._dev.is_kernel_driver_active(0):
			self._dev.detach_kernel_driver(0)
			self._had_driver = True
		self._dev.set_configuration()
		self._dev.ctrl_transfer(0x21, 0x09, 0x0200, 0x00, [0xc4, 0xc6, 0xc0, 0x92, 0x40, 0x23, 0xdc, 0x96])

		self.updateInfo(isOnline)


	def proccedEvent(self, event, isOnline):
		pass


	def updateInfo(self, isOnline):
		try:
			pass
		except Exception as ex:
			self._logger.exception(ex)


	def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
		try:
			pass
		except Exception as ex:
			self._logger.exception(ex)


	def done(self):
		""" """
		usb.util.release_interface(self._dev, 0)
		if self._had_driver:
			self._dev.attach_kernel_driver(0)


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
