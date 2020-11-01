 include ./ghidorah.d 

WHITE equ $CF
YELLOW equ $9F
CYAN equ $DF
GREEN equ $8F
MAGENTA equ $EF
RED equ $BF
BLUE equ $AF
BLACK EQU $80

FO equ RED
BK equ BLACK

 pshs  u
 lda   MyNodex,u
# anda  #$01
# bne   DoC
#DoC
 lda   #'O
 bsr   DrawChar
 puls  u,pc

* lda  #32
*l@
* pshs a
* bsr  Delay
* bsr  ShiftScreenLeft
* puls a
* deca
* bne  l@

 lda  #32
l@
 pshs a
 bsr  Delay
 bsr  ShiftScreenRight
 puls a
 deca
 bne  l@

 rts

Delay ldx #10000
l@ leax -1,x
 bne l@ 
 rts

write
 clrb
l@
 ldu   ,x++
 stu   ,y++
 decb
 bne   l@
 rts

ShiftScreenLeft
 ldx #$400
 lda #16
l@
 pshs a
 bsr ShiftLineLeft
 puls a
 deca
 bne l@
 rts

ShiftLineLeft
 ldd ,x
 pshs d
 ldb #15
l@
 ldu 2,x
 stu ,x
 leax 2,x
 decb
 bne l@
 puls d
 std ,x++
 rts

ShiftScreenRight
 ldx #$400
 lda #16
l@ 
 pshs a
 bsr ShiftLineRight
 puls a
 deca
 bne l@
 rts

ShiftLineRight
 leax 28,x
 ldd 2,x
 pshs d
 ldb #14
l@
 ldu ,x
 stu 2,x
 leax -2,x
 decb
 bne l@
 puls d
 std ,x
 leax 32,x
 rts

DrawChar
  jsr $A928
  ldx #$400
  bra DrawO

DrawC
  ldu #FO*256+FO
  leax 32+3,x

# Draw top of C
  ldb #13
l@ stu ,x++
  decb
  bne l@

# Draw clip of C
  leax 5,x
  stu 26,x

# Draw left side of C
  ldb #12
l@  stu ,x
  leax 32,x
  decb
  bne l@

# Draw clip of C
  leax -32,x
  stu 26,x

# Draw bottom of C
  leax 32,x
  leax 1,x
  ldb #13
l@ stu ,x++
  decb
  bne l@

  rts

DrawO
  bsr DrawC
  ldx #$400+64+28

  ldb #12
l@ stu ,x
  leax 32,x
  decb
  bne l@

  rts
