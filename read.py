# Usage:
#  --readaddr <address> --readlen <read_length> --device <serdev> --baud <baudrate> --nodex <#>
import sys
import ghidorah
import argparse

defaultDevice = '/dev/cu.usbserial-FT079LCR2'
defaultDevice = '/dev/cu.usbserial-USAKMYZM'
defaultDevice = '/dev/cu.usbserial-A2003EyG'

parser = argparse.ArgumentParser(description='Parameters for the command.')
parser.add_argument('--readaddr', type=str, default='0x600',
                    help='address to read (e.g. 0x400, 512)')
parser.add_argument('--readlen', type=str, default='0x10',
                    help='length to read (e.g. 0x100, 256)')
parser.add_argument('--baud', type=int, default=57600,
                    help='baud rate')
parser.add_argument('--device', type=str, default=defaultDevice,
                    help='serial port')
parser.add_argument('--nodex', type=str, default='0xFF',
                    help='nodex (0-254, or 255 (default) for broadcast)')
parser.add_argument('--raw', action='store_true',
                    help='dump values in raw binary')
parser.add_argument('--verbose', action='store_true',
                    help='verbosity')

args = parser.parse_args()
baud = args.baud
device = args.device
readaddr = int(args.readaddr, 0)
readlen = int(args.readlen, 0)
nodex = int(args.nodex, 0)
verbose = args.verbose
raw = args.raw

l = ghidorah.Ghidorah(device, baud, verbose)
b = l.read(nodex, readaddr, readlen)
if raw == False:
	print(b)
else:
	c = bytes(b)
	sys.stdout.buffer.write(c)
