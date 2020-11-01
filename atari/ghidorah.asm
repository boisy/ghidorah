; *****************************
; CIO equates
; *****************************
ICHID  =   $0340
ICDNO  =   $0341
ICCOM  =   $0342
ICSTA  =   $0343
ICBAL  =   $0344
ICBAH  =   $0345
ICPTL  =   $0346
ICPTH  =   $0347
ICBLL  =   $0348
ICBLH  =   $0349
ICAXl  =   $034A
ICAX2  =   $034B
CIOV   =   $E456

.segment "CODE"

; *****************************
; Now we load in required data
; *****************************
	LDX #0        ; Since it's IOCB0
	LDA #9        ; For put record
	STA ICCOM,X   ; Command byte
	LDA #<MSG	  ; Low byte of MSG
	STA ICBAL,X   ;  into ICBAL
	LDA #>MSG	  ; High byte of MSG
	STA ICBAH,X   ;  into ICBAH
	LDA #0        ; Length of MSG
	STA ICBLH,X   ;  high byte
	LDA #$FF      ; Length of MSG
	STA ICBLL,X   ; See discussion
; *****************************
; Now put it to the screen
; *****************************
	JSR CIOV
B:	JMP B
	RTS
; *****************************
; The message itself
; *****************************
MSG:    .asciiz "A SUCCESSFUL WRITE!"
	.byte $9B
