# Usage:
#   --device <serdev> --baud <baudrate>
import serial
import argparse

majorVersion = 0
minorVersion = 9
defaultDevice = '/dev/cu.usbserial-FT079LCR2'
defaultDevice = '/dev/cu.usbserial-USAKMYZM'
defaultDevice = '/dev/cu.usbserial-A2003EyG'

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--baud', type=int, default=57600,
                    help='baud rate')
parser.add_argument('--device', type=str, default=defaultDevice,
                    help='serial port')

args = parser.parse_args()
baud = args.baud
device = args.device
found = False

with serial.Serial(device, baud) as ser:
	while True:
		# wait for a message
		message = ser.read(22)

		command = message[0]
		if command == 'D':
			found = True
			destNodex = message[2] + 1
			message[2] = destNodex
		else:
			if found == True:
				# don't do anything else at the moment
				if command == 'I':
					message[0] = command
					message[3] = majorVersion
					message[4] = minorVersion
					if baud == 57600:
						message[5] = 0
					else:
						message[5] = 1
					message[6:] = "PYTHON    "
				break
			
		res = ''.join(format(x, '02x') for x in message)
		print('Relaying message ', len(message), ' bytes: ', res)

		# relay the message
		ser.write(message)
