# Usage:
#   --device <serdev> --baud <baudrate> --nodex <#>
import ghidorah
import argparse

defaultDevice = '/dev/cu.usbserial-FT079LCR2'
defaultDevice = '/dev/cu.usbserial-USAKMYZM'
defaultDevice = '/dev/cu.usbserial-A2003EyG'

parser = argparse.ArgumentParser(description='Parameters for the command.')
parser.add_argument('--baud', type=int, default=57600,
                    help='baud rate')
parser.add_argument('--device', type=str, default=defaultDevice,
                    help='serial port')
parser.add_argument('--nodex', type=str, default='0xFF',
                    help='nodex (0-254, or 255 (default) for broadcast')
parser.add_argument('--verbose', action='store_true',
                    help='verbosity')

args = parser.parse_args()
baud = args.baud
device = args.device
nodex = int(args.nodex, 0)
verbose = args.verbose

# 1. perform discovery and get # of listeners
l = ghidorah.Ghidorah(device, baud, verbose)
listeners = l.discovery()
print('Number of listeners =', listeners)

# 2. get the identity of each listener and find their maximum baud rate
maxBaudRate = 57600
for nodex in range(1, listeners + 1):
	mtyp = l.identity(nodex)
	if mtyp == 'CC3':
		mbau = 115200
	else:
		mbau = 57600
	print('Nodex', nodex, ', machine type =', mtyp)

# 3. if every listener has a maximum baud rate of 115.2kbps, set them up with that rate
#if maxBaudRate == 1:
#	data = [0x7F, 0xFF, 0xD9, 0x39]
#	ghidorah.write(device, baud, 0xFF, 0x1200, 0x4, data)
#	ghidorah.exec(device, baud, 0xFF, 0x1200)
