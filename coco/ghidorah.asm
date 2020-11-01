********************************************************************
* Ghidorah - Listener client for the CoCo
*
* This is the CoCo "firmware" that implements the Ghidorah protocol.
* 
* $Id$
*
* ------------------------------------------------------------------
*          2020/03/15  Boisy G. Pitre
* Started.

         nam   Ghidorah
         ttl   Listener client for the CoCo

         use   ./ghidorah.d

OUTPUT   EQU   1

         IFNE  DISKROM
Top      equ   $C000
         ELSE
Top      equ   $7C00
         ENDC
 
         org   Top

         IFNE  DISKROM
         fcc   "DK"
         lbra  Entry
         fill  $FF,9*256		spaced out to prevent CoCo 3 BASIC ROM patches
         ELSE
         ENDC

* Entry point
Entry    orcc  #IntMasks		disable FIRQ, IRQ
         leas  -end,s           carve out space above stack for statics
         tfr   s,u              point U to statics area

* Initialize vars
         clr   FoundMe,u        we just started, so we haven't been discovered

         IFNE  OUTPUT
         jsr   $A928
         leax  SignOn,pcr
l@       lda   ,x+
         beq   x@
         jsr   [$A002]
         bra   l@
x@
         ENDC

* MAIN PROCESSING LOOP
* This is the heart of the listener
WaitForMessage
         leax  Message,u                point to the message buffer
         ldy   #MessageSz               read in...
         lbsr  DWRead                   ...the next message
         bcs   WaitForMessage           ...if error, continue reading
         bne   WaitForMessage           ...if timeout, continue reading

* We have a message -- process it.
         lda   ,x			grab command from message
         cmpa  #MSGDSCVR		discover message?
         lbeq  Discover			branch if so
         tst   FoundMe,u                did I get discovered yet?
         beq   Complain                 if not, just complain
         ldb   2,x                      else check destination nodex
         cmpb  MyNodex,u                is this message for me?
         beq   Act                      yes, act on it
         cmpb  #$FF                     is it for everyone?
         bne   Relay                    no... relay it to the next listener
  
* A = message command
Act      cmpa  #MSGREAD                 read message?
         beq   ReadWrite                branch if so
         cmpa  #MSGWRITE                write message?
         beq   ReadWrite                branch if so
         cmpa  #MSGEXEC                 exec message?
         beq   Exec                     branch if so
         cmpa  #MSGIDENT                identity message?
         beq   Identity                 branch if so

* Unknown command -- just relay it
Complain
         IFNE  OUTPUT
         lda   #'?
         jsr   [$A002]
         ENDC

Relay
         ldy   #MessageSz
         lbsr  DWWrite
         bra   WaitForMessage


* This routine handles both Read and Write messages
ReadWrite
         IFNE  OUTPUT
         jsr   [$A002]
         ENDC

         ldb   5,x                     get read/write limit
         cmpb  #1                      limit < 1?
         blt   Relay                   if so, ignore
         cmpb  #DataSize               limit > DataSize?
         bgt   Relay                   if so, ignore 
         ldy   3,x                     get address in Y
         pshs  x                       save off X (Message Pointer) on stack for now
         leax  6,x                     point to data payload area of message
         cmpa  #MSGWRITE               if write message...
         beq   DoWrite                 ...do it

* Read message loop
DoRead
loop@    lda   ,y+                     loop: copy from Y (then increment) into A
         sta   ,x+                     ... and from A into X (then increment)
         decb                          got it all?
         bne   loop@                   continue if not
         bra   CleanUp

* Write message loop
DoWrite
loop@    lda   ,x+                     loop: copy from Y (then increment) into A
         sta   ,y+                     ... and from A into X (then increment)
         decb                          got it all?
         bne   loop@                   continue if not

CleanUp  puls  x                       get saved X off stack
         bra   Relay                   and relay

Exec
         IFNE  OUTPUT
         jsr   [$A002]
         ENDC

* For Exec, do Relay FIRST, and THEN the JMP
         pshs  d,x,y,u                 save off regs
         ldy   #MessageSz              do the relay now
         lbsr  DWWrite
         ldx   2,s                     recover the message pointer
         jsr   [3,x]                   JSR to the exec address
* Optimistic that an RTS will give us back control
         puls  d,x,y,u                 recover saved regs
         lbra  WaitForMessage          wait for another message

* A = Identity Command, X = Pointer to Message
Identity
         IFNE  OUTPUT
         jsr   [$A002]
         ENDC

         pshs  x                       save off message ptr
         leax  3,x
         ldd   #"CC                    this...
         std   ,x++                    is a CoCo!
         lda   $FFA0                   but is it a CoCo 3?
         cmpa  #$38
         bne   coco12                 branch if not
         lda   #'3
         bra   cont
coco12   lda   #'?
cont     sta   ,x+
         ldb   #13
l@       clr   ,x+
         decb
         bne   l@
         puls  x
         bra  Relay

* A = Discovery Command, X = Pointer to Message
Discover
         inc   2,x                     increment nodex in message
         ldb   2,x                     get in B
         stb   MyNodex,u               save it off in our statics

         IFNE  OUTPUT
         lda   #'D
         jsr   [$A002]
         tfr   b,a
         lbsr  Hex8Bit
         ENDC

         lda   #1
         sta   FoundMe,u                mark that we've been discovered
         lbra  Relay

CopyRtn  clra
         tfr   d,x
Copy1    ldb   ,u+
         stb   ,y+
         leax  -1,x
         bne   Copy1
         rts

         IFEQ  DW4-1
         use   ./dw4read.asm 
         use   ./dw4write.asm 
         ELSE
         use   ./dwread.asm 
         use   ./dwwrite.asm 
         ENDC

         IFNE  OUTPUT
* Destroys A
HexNibble
         anda  #%00001111
         cmpa  #$09
         bgt   ha@
         adda  #'0
         bra   hc@
ha@      adda  #'A-10
hc@      jmp   [$A002]

* Destroys A
Hex8Bit
         pshs  a
         lsra
         lsra
         lsra
         lsra
         bsr   HexNibble
         puls  a
         bra   HexNibble
 
* Destroys A
Hex16Bit
         pshs  d
         bsr   Hex8Bit
         puls  d
         tfr   b,a
         bra   Hex8Bit
         ENDC

         IFNE  OUTPUT
SignOn   fcc   /GHIDORAH /
         fcb   MAJOR+$30
         fcc   /./
         fcb   MINOR+$30
         fcb   $0D
         fcb   $00
         ENDC

eom      equ   *

         IFNE  DSKROM
* Fill pattern
 fdb eom
         fill   $FF,$2000-eom+19
         ENDC

         end   Entry

