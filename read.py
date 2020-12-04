# Usage:
#  --readaddr <address> --readlen <read_length> --device <serdev> --baud <baudrate> --nodex <#>
import ghidorah
import argparse

defaultDevice = '/dev/cu.usbserial-FT079LCR2'
defaultDevice = '/dev/cu.usbserial-USAKMYZM'
defaultDevice = '/dev/cu.usbserial-A2003EyG'

parser = argparse.ArgumentParser(description='Parameters for the command.')
parser.add_argument('--readaddr', type=str, default='0x600',
                    help='address to read')
parser.add_argument('--readlen', type=str, default='0x10',
                    help='length to read')
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
readaddr = int(args.readaddr, 0)
readlen = int(args.readlen, 0)
nodex = int(args.nodex, 0)
verbose = args.verbose

l = ghidorah.Ghidorah(device, baud, verbose)
(error, bytes) = l.read(nodex, readaddr, readlen)
if error == -1:
	print("Timeout error")
	exit(0)
print(bytes)
