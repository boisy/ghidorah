# Ghidorah

Ghidorah is a protocol for passing information between computers linked together using a specially constructed RS-232 cable. Ghidorah employs a ring topology; each computer on the ring uses Cooperative Message Passing (CMP) to ensure that the message finds its way to its intended destination. The message's routing path is complete when the arbiter receives the message back from its round trip.

The TRS-80 Color Computer family is currently supported, but in theory, any computer with an RS-232 port can be part of the ring.

## Definitions

* Arbiter: a computer on the ring that is responsible for originating messages. There can only be one arbiter. An arbiter's nodex is always 0.
* Listener: a computer on the ring that listens for messages. A listener's nodex can be between 1 and 254.
* Message: a stream of data that has both a header and a data payload.
* Nodex: a number between 0 and 254 that uniquely identifies a node on the ring.
* Ring: the physical cable that connects the arbiter and listeners together.

## Commands

There are Python 3 commands for several common operations.

For convenience, you can set the `GHIDORAH_DEVICE` environment variable on the arbiter to the serial device. 

### Discover

This is the first message that should be sent to all listeners on the ring. This forces each listener to assign itself an ID, and tells the arbiter how many listeners are on the ring.

Note: If any other message is sent prior to this one, the listeners ignore it!

Example:

`python3 discover.py --device /dev/cu.usbserial-FTVCW8GB0 --baud 57600`

Replace the device with the appropriate name for your arbiter. You can leave off the `--baud 57600` since it's the default.

### Identity

This command identifies the type of machine that is listening.

Note: If any other message is sent prior to this one, the listeners ignore it!

Example 1: Identify all listeners on the ring.

`python3 identify.py --device /dev/cu.usbserial-FTVCW8GB0`

Example 2: Identify a particular listener on the ring.

`python3 identify.py --device /dev/cu.usbserial-FTVCW8GB0 --nodex 2`

### Setup

This command can be used in place of `discover.py` since it does a Discovery, performs an Identity, and if there are only CoCo 3s on the ring, puts them in high-speed mode. In that case, subsequent commands should use `--baud 115200`.

Example: Setup all listeners on the ring.

`python3 setup.py --device /dev/cu.usbserial-FTVCW8GB0`

### Read
This command reads memory from a listener and returns the bytes.

Example: Read 256 bytes from location $6000 from listener 1:

`python3 read.py --device /dev/cu.usbserial-FTVCW8GB0 --readaddr 0x6000 --readlen 0x100 --nodex 1`

### Load
This command writes bytes to a listener's memory. Optionally, it can execute at an address.               

Example 1: Load the contents of the file `test.raw` into the memory of listener 3 at address $0700:

`python3 load.py --device /dev/cu.usbserial-FTVCW8GB0 --file test.raw --loadaddr 0x700 --nodex 3`

Example 2: Load the contents of the file `game.raw` into the memory of listener 3 at address $0700 and execute at that address:

`python3 load.py --device /dev/cu.usbserial-FTVCW8GB0 --file game.raw --loadaddr 0x700 --execaddr 0x700 --nodex 3`

### LoadM
This command behaves similar to the Load command, except that it can properly load Disk BASIC compatible .BIN files. Also, the code will automatically execute once loaded.

Example: Load the contents of the file `LANCER.BIN` into the memory of listener 2 and start the game:

`python3 loadm.py --device /dev/cu.usbserial-FTVCW8GB0 --file LANCER.BIN --nodex 2`

## Messages

Ghidorah uses messages to pass information between listeners. Here are the supported messages:

### Discovery Message

The Discovery Message is sent by the arbiter to discover who is on the ring. It must be the first message a listener receives. If a listener receives any other message before the Discovery Message, it will ignore that message and simply relay it to the next listener.

* Byte 0: <0x44>
* Byte 1: <Source Nodex>
* Byte 2: 0
* Bytes 3 to 21: Don't Care

Each listener that receives the message shall:

  1. Increment the value in Byte 2.
  2. Obtain the incremented value in Byte 2 and save it as its nodex.
  3. Send the message to the next listener.

Once the arbiter receives the message, it may investigate Byte 2 which holds the number of listeners on the ring.

### Identity Message

The Identity Message is sent by the arbiter to determine specific information about a listener.

* Byte 0: <0x49>
* Byte 1: <Source Nodex>
* Byte 2: <Destination Nodex> (0 to 254, or 255 for everyone)
* Bytes 3 to 21: Don't Care

Each listener shall examine Byte 2 and compare it to its nodex. If there is no match, the listener shall:

  1. Send the message to the next listener.

If the nodex matches, the listener shall:

  1. Set Byte 3 to the major revision of the client software.
  2. Set Byte 4 to the minor revision of the client software.
  3. Set Byte 5 to the maximum supported baud rate (0 = 57600, 1 = 115200).
  4. Set Bytes 6 to 15 to a 10 character string identifying the machine type.
  5. Send the message to the next listener.

### Read Message

The Read Message is sent by the arbiter to obtain data from memory for a given listener.

* Byte 0: <0x52>
* Byte 1: <Source Nodex>
* Byte 2: <Destination Nodex> (0 to 254, or 255 for everyone)
* Byte 3: Bits 15 to 8 of read address
* Byte 4: Bits 7 to 0 of read address
* Byte 5: Read limit (1 to 16)
* Bytes 6 to 21: Don't Care

Each listener shall examine Byte 2 and compare it to its nodex. If there is no match, the listener shall:

  1. Send the message to the next listener.

If the nodex matches, the listener shall:

  1. Obtain the 16 bit address in Bytes 3 and 4 and the limit in Byte 5.
  2. Copy 'limit' bytes from its memory at the specified address to Bytes 6 to (5+'limit') in the message.
  3. Send the message to the next listener.

### Write Message

The Write Message is sent by the arbiter to write data to memory for a given listener.

* Byte 0: <0x57>
* Byte 1: <Source Nodex>
* Byte 2: <Destination Nodex> (0 to 254, or 255 for everyone)
* Byte 3: Bits 15 to 8 of write address
* Byte 4: Bits 7 to 0 of write address
* Byte 5: Write limit (1 to 16)
* Bytes 6 to 21: Data to write

Each listener shall examine Byte 2 and compare it to its nodex. If there is no match, the listener shall:

  1. Send the message to the next listener.

If the nodex matches, the listener shall:

  1. Obtain the 16 bit address in Bytes 3 and 4 and the limit in Byte 5.
  2. Copy 'limit' bytes from Bytes 6 to (5+'limit') of the message to its memory at the specified address.
  3. Send the message to the next listener.

### Execute Message

The Execute Message is sent by the arbiter to direct the listener to start executing at an address in its memory.

* Byte 0: <0x45>
* Byte 1: <Source Nodex>
* Byte 2: <Destination Nodex> (0 to 254, or 255 for everyone)
* Byte 3: Bits 15 to 8 of execution address
* Byte 4: Bits 7 to 0 of execution address
* Bytes 5 to 21: Don't care

Each listener shall examine Byte 2 and compare it to its nodex. If there is no match, the listener shall:

  1. Send the message to the next listener.

If the nodex matches, the listener shall:

  1. Obtain the 16 bit address in Bytes 3 and 4.
  2. Send the message to the next listener.
  3. Direct its CPU to start executing at the specified address.

