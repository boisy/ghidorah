# Usage:
#   --file <file> --loadaddr <address> --device <serdev> --baud <baudrate> --nodex <#> --execaddr <address> --verbose
import ghidorah
import argparse

defaultDevice = '/dev/cu.usbserial-FT079LCR2'
defaultDevice = '/dev/cu.usbserial-USAKMYZM'
defaultDevice = '/dev/cu.usbserial-A2003EyG'

parser = argparse.ArgumentParser(description='Parameters for the command.')
parser.add_argument('--fast', action='store_true',
                    help='load in fast mode (115.2kbps)')
parser.add_argument('--file', type=str, default='file',
                    help='file to load')
parser.add_argument('--offset', type=str, default='0',
                    help='offset to load file')
parser.add_argument('--execaddr', type=str, default='0x0',
                    help='address to execute ')
parser.add_argument('--baud', type=int, default=57600,
                    help='baud rate')
parser.add_argument('--device', type=str, default=defaultDevice,
                    help='serial port')
parser.add_argument('--nodex', type=str, default='0xFF',
                    help='nodex 0-254, or 255 for broadcast (default)')
parser.add_argument('--verbose', action='store_true',
                    help='verbosity')

args = parser.parse_args()
baud = args.baud
device = args.device
file = args.file
offset = int(args.offset, 0)
execaddr = int(args.execaddr, 0)
nodex = int(args.nodex, 0)
verbose = args.verbose
fast = args.fast

if fast == True:
	baud = 57600

l = ghidorah.Ghidorah(device, baud, verbose)

if fast == True:
	#l.write(nodex, 0xFFD9, 0x1, [0x00])
	l.write(nodex, 0x600, 0x4, [0x7F, 0xFF, 0xD9, 0x39])
	l.execute(nodex, 0x600)
	l.baud = 115200
		
execaddr = l.loadm(nodex, file, offset, -1)

if fast == True:
	#l.write(nodex, 0xFFD8, 0x1, [0x00])
	l.write(nodex, 0x600, 0x4, [0x7F, 0xFF, 0xD8, 0x39])
	l.execute(nodex, 0x600)
	l.baud = 57600

l.execute(nodex, execaddr)
