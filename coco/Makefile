
DEPENDS		= ./Makefile

AS		= lwasm -r --pragma=condundefzero
ASOUT		= -o
ECHO		= echo
MAKEWAV		= makewav -r -c

BINS		= ghidorah.raw colorbar.raw c.raw o.raw
ROMS		= ghidorah.rom
DSKS            = ghidorah.dsk
WAVS            = ghidorah.wav

all:	banner raw dsk rom wav $(DEPENDS)

banner:
	@$(ECHO) "**************************"
	@$(ECHO) "*                        *"
	@$(ECHO) "*        GHIDORAH        *"
	@$(ECHO) "*                        *"
	@$(ECHO) "**************************"

dsk:	ghidorah.asm
	$(AS) $(ASOUT)/tmp/ghidorah.bin ghidorah.asm $(AFLAGS) -DBIN --decb
	decb dskini ghidorah.dsk
	decb copy autoexec.bas ghidorah.dsk,AUTOEXEC.BAS -0 -t
	decb copy -2 /tmp/ghidorah.bin ghidorah.dsk,GHIDORAH.BIN

raw:	ghidorah.asm colorbar.asm
	$(AS) $(ASOUT)ghidorah.raw ghidorah.asm $(AFLAGS)
	$(AS) $(ASOUT)colorbar.raw colorbar.asm $(AFLAGS)
	$(AS) $(ASOUT)co.raw co.asm $(AFLAGS)

rom:	ghidorah.asm
	$(AS) $(ASOUT)ghidorah.rom $< $(AFLAGS) -DDISKROM
	os9 padrom 8192 ghidorah.rom

wav:	ghidorah.asm
	$(AS) $(ASOUT)/tmp/ghidorah.cas $< $(AFLAGS) -DBIN --format=srec
	makewav -l0 /tmp/ghidorah.cas -oghidorah.wav

clean:
	-rm $(BINS) $(ROMS) $(DSKS) $(WAVS)

loademu: rom
	#python3 ../../ostrich2/ostrich2.py --device /dev/cu.usbserial-A100K8WY setbank 0
	cat ghidorah.rom ghidorah.rom ghidorah.rom ghidorah.rom >> /tmp/ghidorah.rom.32k
	python3 ../../ostrich2/ostrich2.py --device /dev/cu.usbserial-A100K8WY write --address 0x8000 < /tmp/ghidorah.rom.32k
