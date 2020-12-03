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

l = ghidorah.Ghidorah(device, baud, verbose)
mtype = l.identity(nodex)
if mtype == "":
	print("no response.")
else:
	print(mtype)
