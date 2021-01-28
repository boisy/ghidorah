
DEPENDS		= ./Makefile

AS		= lwasm -r --pragma=condundefzero
ASOUT		= -o
ECHO		= echo
MAKEWAV		= makewav -r -c

BINS		= ghidorah.bin colorbar.bin co.bin
ROMS		= ghidorah.rom
DSKS            = ghidorah.dsk
WAVS            = ghidorah.wav

all:	banner bin dsk rom wav $(DEPENDS)

banner:
	@$(ECHO) "**************************"
	@$(ECHO) "*                        *"
	@$(ECHO) "*        GHIDORAH        *"
	@$(ECHO) "*                        *"
	@$(ECHO) "**************************"

dsk:	bin
	decb dskini ghidorah.dsk
	decb copy autoexec.bas ghidorah.dsk,AUTOEXEC.BAS -0 -t
	decb copy -2 ghidorah.bin ghidorah.dsk,GHIDORAH.BIN
	decb copy -2 colorbar.bin ghidorah.dsk,COLORBAR.BIN
	decb copy -2 co.bin ghidorah.dsk,CO.BIN

bin:	ghidorah.asm colorbar.asm co.asm
	$(AS) $(ASOUT)ghidorah.bin ghidorah.asm $(AFLAGS) --decb
	$(AS) $(ASOUT)colorbar.bin colorbar.asm $(AFLAGS) --decb
	$(AS) $(ASOUT)co.bin co.asm $(AFLAGS) --decb

rom:	ghidorah.asm
	$(AS) $(ASOUT)ghidorah.rom $< $(AFLAGS) -DDISKROM
	os9 padrom 8192 ghidorah.rom

wav:	ghidorah.asm
	$(AS) $(ASOUT)/tmp/ghidorah.cas $< $(AFLAGS) --format=srec
	makewav -l0 /tmp/ghidorah.cas -oghidorah.wav

clean:
	-rm $(BINS) $(ROMS) $(DSKS) $(WAVS)

loademu: rom
	#python3 ../../ostrich2/ostrich2.py --device /dev/cu.usbserial-A100K8WY setbank 0
	cat ghidorah.rom ghidorah.rom ghidorah.rom ghidorah.rom >> /tmp/ghidorah.rom.32k
	python3 ../../ostrich2/ostrich2.py --device /dev/cu.usbserial-A100K8WY write --address 0x8000 < /tmp/ghidorah.rom.32k
