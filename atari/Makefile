
DEPENDS		= ./Makefile

AS			= ca65
LD			= ld65
ASOUT		= -o
ECHO		= echo
MAKEWAV		= makewav -r -c

#BINS		= colorbar.raw
ROMS		= ghidorah.rom

all:	banner ghidorah.rom $(DEPENDS)

banner:
	@$(ECHO) "**************************"
	@$(ECHO) "*                        *"
	@$(ECHO) "*        GHIDORAH        *"
	@$(ECHO) "*                        *"
	@$(ECHO) "**************************"

ghidorah.rom:	ghidorah.asm
	$(AS) $(ASOUT) ghidorah.o ghidorah.asm $(AFLAGS)
	$(LD) -C atari.cfg ghidorah.o -o ghidorah.rom

clean:
	-rm $(BINS) $(ROMS) ghidorah.o

loademu: rom
	#python3 ../../ostrich2/ostrich2.py --device /dev/cu.usbserial-A100K8WY setbank 0
	cat ghidorah.rom ghidorah.rom ghidorah.rom ghidorah.rom >> /tmp/ghidorah.rom.32k
	python3 ../../ostrich2/ostrich2.py --device /dev/cu.usbserial-A100K8WY write --address 0x8000 < /tmp/ghidorah.rom.32k
