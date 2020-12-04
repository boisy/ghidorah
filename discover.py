# Usage:
#   --device <serdev> --baud <baudrate>
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
parser.add_argument('--verbose', action='store_true',
                    help='verbosity')

args = parser.parse_args()
baud = args.baud
device = args.device
verbose = args.verbose

m = ghidorah.Ghidorah(device, baud, verbose)
(error, numberOfListeners) = m.discovery()
if error == -1:
	print("Timeout error")
	exit(0)

print('All listeners initialized. Number of listeners: ' + str(numberOfListeners))
