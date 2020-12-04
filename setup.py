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
                    help='nodex (0-254, or 255 for broadcast (default)')
parser.add_argument('--verbose', action='store_true',
                    help='verbosity')

args = parser.parse_args()
baud = args.baud
device = args.device
nodex = int(args.nodex, 0)
verbose = args.verbose

# 1. perform discovery and get # of listeners
l = ghidorah.Ghidorah(device, baud, verbose)
(error, listeners) = l.discovery()
if error == -1:
	print("Timeout error")
	exit(0)
print('Number of listeners =', listeners)

# 2. get the identity of each listener and find their maximum baud rate
numCC3s = 0
numCC2s = 0
for nodex in range(1, listeners + 1):
	mtyp = l.identity(nodex)
	if mtyp == 'CC3':
		numCC3s = numCC3s + 1
		print('Nodex', nodex, ', machine type = CoCo 3')
	else:
		numCC2s = numCC2s + 1
		print('Nodex', nodex, ', machine type = CoCo 1/2')

# 3. if every listener has a maximum baud rate of 115.2kbps, set them up with that rate
print("No. of CoCo 1/2s: ", numCC2s, ", No. of CoCo 3s: ", numCC3s)
if numCC2s == 0:
	# We only have CoCo 3s. Kick them into high speed
	# clr $FFD9; rts
	l.write(nodex, 0x600, [0x7F, 0xFF, 0xD9, 0x39])
	l.execute(nodex, 0x600)
