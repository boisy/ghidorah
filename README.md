# Ghidorah

Ghidorah is a protocol for passing information between computers linked together via a special RS-232 cable. Ghidorah employs a ring topology; each computer on the ring uses Cooperative Message Passing (CMP) to ensure that the message finds its way to its intended destination. The message's routing path is complete when the arbiter receives the message back from its round trip.

The TRS-80 Color Computer family is currently supported, but in theory, any computer with an RS-232 port can be part of the ring.

## Definitions

* Arbiter: a computer on the ring that is responsible for originating messages. There can only be one arbiter. An arbiter's nodex is always 0.
* Listener: a computer on the ring that listens for messages. A listener's nodex can be between 1 and 254.
* Message: a stream of data that has both a header and a data payload.
* Nodex: a number between 0 and 254 that uniquely identifies a node on the ring.
* Ring: the physical cable that connects the arbiter and listeners together.

## Messages

Ghidorah uses messages to pass information between listeners. Here are the supported messages:

### Discovery Message

The Discovery Message is sent by the arbiter to discover who is on the ring. It must be the first message a listener receives. If a listener receives any other message before the Discovery Message, it will ignore that message and simply relay it to the nnext listener.

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

