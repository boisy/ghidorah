import serial

class Ghidorah(object):

	read_timeout = 1.0
	message_size = 22

	def __init__(self, device, baud = 57600, verbose = 1):
		self.device = device
		self.baud = baud
		self.verbose = verbose

	def discovery(self):
		message = bytearray([0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
		with serial.Serial(self.device, self.baud) as ser:
			ser.timeout = self.read_timeout

			self.logOutboundMessage(message)

			# send out the message
			ser.write(message)

			# wait for the response
			response = ser.read(self.message_size)

			numberOfListeners = -1

			if len(response) == self.message_size:
				# the # of listeners is at byte offset 2
				numberOfListeners = response[2]

				self.logInboundMessage(response)

		return numberOfListeners


	def identity(self, nodex):
		message = bytearray([0x49, 0x00, nodex, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
		with serial.Serial(self.device, self.baud) as ser:
			ser.timeout = self.read_timeout
			self.logOutboundMessage(message)
	
			# send out the message
			ser.write(message)
	
			# wait for the response
			response = ser.read(self.message_size)
	
			if len(response) == self.message_size:
				self.logInboundMessage(response)

				machineType = response[3:21].decode('ASCII')
	
				return machineType
			else:
				return (-1, -1, "")

	def read(self, nodex, readaddr, readlen):
		message = bytearray([0x52, 0x00, nodex, 0x00, 0x00, 0x00, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0x0AA, 0x55])

		with serial.Serial(self.device, self.baud) as ser:
			ser.timeout = self.read_timeout
			for x in range(readaddr, readaddr + readlen, 16):
				message[3] = int(x / 256)
				message[4] = int(x % 256)
				message[5] = 16
		
				self.logOutboundMessage(message)
		
				# send out the message
				ser.write(message)
	
				# wait for the response
				response = ser.read(self.message_size)
				if len(response) == self.message_size:
					message[6:] = response[6:]

					self.logInboundMessage(response)
	

	def write(self, nodex, writeaddr, writelen, data):
		message = [0x57, 0x00, nodex, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

		l = len(data)
		message[3] = int(writeaddr / 256)
		message[4] = int(writeaddr % 256)
		message[5] = l
		message[6:6+l] = data

		self.logOutboundMessage(message)
	
		with serial.Serial(self.device, self.baud) as ser:
			ser.timeout = self.read_timeout
			# send out the message
			ser.write(message)

			# wait for the response
			response = ser.read(self.message_size)
			self.logInboundMessage(response)


	def _exec(self, nodex, execaddr):
		message = [0x45, 0x00, nodex, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
	
		with serial.Serial(self.device, self.baud) as ser:
			ser.timeout = self.read_timeout
			message[3] = int(execaddr / 256)
			message[4] = int(execaddr % 256)
		
			self.logOutboundMessage(message)

			# send out the message
			ser.write(message)
	
			# wait for the response
			response = ser.read(self.message_size)
			self.logInboundMessage(response)


	def load(self, nodex, file, loadaddr, execaddr):
		message = [0x57, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
		message[1] = nodex

		f = open(file, "rb")
		while True:
			bytes = f.read(16)
			if len(bytes) == 0:
				break;
			l = len(bytes)

			self.write(nodex, loadaddr, l, bytes)
			loadaddr = loadaddr + l

		# Execute only if execaddr != 0
		if execaddr != 0:
			self._exec(nodex, execaddr)	

	def messageToString(self, message):
		res = ''.join(format(x, '02x') for x in message)
		return res

	def log(self, logText):
		if self.verbose > 0:
			print(logText)

	def logInboundMessage(self, message):
		if self.verbose > 0:
			r = self.messageToString(message)
			print('<-' + r)

	def logOutboundMessage(self, message):
		if self.verbose > 0:
			r = self.messageToString(message)
			print('->' + r)
