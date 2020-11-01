# Usage:
#   --device <serdev> --baud <baudrate>
import ghidorah
import argparse

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

m = ghidorah.Ghidorah(device, baud)
numberOfListeners = m.discovery()
print('All listeners initialized. Number of listeners: ' + str(numberOfListeners))
