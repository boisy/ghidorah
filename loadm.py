# Usage:
#   --file <file> --loadaddr <address> --device <serdev> --baud <baudrate> --nodex <#> --execaddr <address> --verbose
import ghidorah
import argparse

defaultDevice = '/dev/cu.usbserial-FT079LCR2'
defaultDevice = '/dev/cu.usbserial-USAKMYZM'
defaultDevice = '/dev/cu.usbserial-A2003EyG'

parser = argparse.ArgumentParser(description='Parameters for the command.')
parser.add_argument('--file', type=str, default='file',
                    help='file to load')
parser.add_argument('--loadaddr', type=str, default='0x600',
                    help='address to load file')
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
loadaddr = int(args.loadaddr, 0)
execaddr = int(args.execaddr, 0)
nodex = int(args.nodex, 0)
verbose = args.verbose

l = ghidorah.Ghidorah(device, baud, verbose)
l.loadm(nodex, file, loadaddr, execaddr)

