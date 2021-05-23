********************************************************************
* listener.d - Listener definitions
*
* $Id$
*
* ------------------------------------------------------------------
*          2020/03/15  Boisy G. Pitre
* Started.

MAJOR    equ   1
MINOR    equ   0

IntMasks equ   $50
V.SCF    equ   0
Vi.PkSz  equ   0

         use   ./dwdefs.d

DataSize equ   16
MessageSz equ DataSize+6

MSGWRITE  EQU   'W'
MSGIDENT  EQU   'I'
MSGREAD   EQU   'R'
MSGEXEC   EQU   'E'
MSGDSCVR  EQU   'D'

* Static memory
         org   0
Message  rmb   MessageSz        ; Message buffer
MyNodex  rmb   1                ; Nodex for this listener
FoundMe  rmb   1                ; 0/1 = discovery hasn't/has happened
end      equ   .

