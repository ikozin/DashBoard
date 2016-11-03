import sys
import time
import threading
import usb.core
import usb.util

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
		self._event_stop = threading.Event()
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
		self._event_stop.set()


	def run(self):
		self._dev.ctrl_transfer(self.REQUEST_TYPE_SEND, self.REQ_HID_SET_REPORT, self.HID_REPORT_TYPE_FEATURE, 0x00, self.magic_buf, self.RW_TIMEOUT)
		while not self._event_stop.isSet():
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

if __name__ == "__main__":
	t_mt8057 = mt8057()
	t_mt8057.start()

	time.sleep(5)
	(valueCO2, valueTemp) = t_mt8057.get_data()
	print(valueCO2, valueTemp)

	time.sleep(5)
	(valueCO2, valueTemp) = t_mt8057.get_data()
	print(valueCO2, valueTemp)

	time.sleep(5)
	(valueCO2, valueTemp) = t_mt8057.get_data()
	print(valueCO2, valueTemp)

	t_mt8057.stop()
	t_mt8057.join()
	print("Done!")
