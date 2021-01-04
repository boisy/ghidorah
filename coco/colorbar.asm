WHITE equ $CF
YELLOW equ $9F
CYAN equ $DF
GREEN equ $8F
MAGENTA equ $EF
RED equ $BF
BLUE equ $AF
BLACK equ $80

ExecAddr equ $6000
 org ExecAddr

 jsr $a928

 ldx #$400

 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write
 bsr write

 bsr write2

 rts

write
 ldu #WHITE*256+WHITE
 stu ,x++
 stu ,x++
 ldu #YELLOW*256+YELLOW
 stu ,x++
 stu ,x++
 ldu #CYAN*256+CYAN
 stu ,x++
 stu ,x++
 ldu #GREEN*256+GREEN
 stu ,x++
 stu ,x++
 ldu #MAGENTA*256+MAGENTA
 stu ,x++
 stu ,x++
 ldu #RED*256+RED
 stu ,x++
 stu ,x++
 ldu #BLUE*256+BLUE
 stu ,x++
 stu ,x++
 ldu #WHITE*256+WHITE
 stu ,x++
 stu ,x++

 rts

write2
 ldu #BLUE*256+BLUE
 stu ,x++
 stu ,x++
 ldu #BLACK*256+BLACK
 stu ,x++
 stu ,x++
 ldu #MAGENTA*256+MAGENTA
 stu ,x++
 stu ,x++
 ldu #BLACK*256+BLACK
 stu ,x++
 stu ,x++
 ldu #CYAN*256+CYAN
 stu ,x++
 stu ,x++
 ldu #BLACK*256+BLACK
 stu ,x++
 stu ,x++
 ldu #WHITE*256+WHITE
 stu ,x++
 stu ,x++
 ldu #BLACK*256+BLACK
 stu ,x++
 stu ,x++

 rts

 END ExecAddr
