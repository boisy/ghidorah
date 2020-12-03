import serial

class Ghidorah(object):
	messageDataLength = 16
	
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

				machineType = response[3:21].decode('ASCII').replace('\00', '')

				return machineType
			else:
				return (-1, -1, "")

	def read(self, nodex, readaddr, readlen):
		message = bytearray([0x52, 0x00, nodex, 0x00, 0x00, 0x00, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0x0AA, 0x55])

		with serial.Serial(self.device, self.baud) as ser:
			ser.timeout = self.read_timeout
			for x in range(readaddr, readaddr + readlen, self.messageDataLength):
				message[3] = int(x / 256)
				message[4] = int(x % 256)
				message[5] = self.messageDataLength
		
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


	# Execute at a specific address
	def execute(self, nodex, execaddr):
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

	# Load raw binary data into memory
	def load(self, nodex, file, loadaddr, execaddr):
		f = open(file, "rb")
		while True:
			bytes = f.read(self.messageDataLength)
			if len(bytes) == 0:
				break;
			l = len(bytes)

			self.write(nodex, loadaddr, l, bytes)
			loadaddr = loadaddr + l

		# Execute only if execaddr != 0
		if execaddr != 0:
			self.execute(nodex, execaddr)	

	# Load a Disk BASIC BIN file (supports segmented BIN files as well)
	def loadm(self, nodex, file, loadaddr, execaddr = -1):
		f = open(file, "rb")
		try: 
			while True:
				bytes = f.read(5)
				segsize = bytes[1] * 256 + bytes[2]
				orgaddr = bytes[3] * 256 + bytes[4]
				if segsize == 0:
					# orgaddr is execaddr
					if execaddr == 0:
						execaddr = orgaddr
					break
				left = segsize
				while left > 0:
					readchunk = min(self.messageDataLength, left)
					left = left - readchunk
					bytes = f.read(readchunk)
					if len(bytes) == 0:
						break;
					l = len(bytes)

					self.write(nodex, orgaddr, l, bytes)
					orgaddr = orgaddr + l
		except EOFError:
			pass
			
		# Execute only if execaddr != 0
		if execaddr != 0:
			self.execute(nodex, execaddr)	

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
