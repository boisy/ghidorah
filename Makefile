DEVICE = /dev/cu.usbserial-FTVCW8GB0
EMUDEVICE = /dev/cu.usbserial-A100K8WY

all:
	cd coco; make

clean:
	cd coco; make clean

discover:
	python3 discover.py --device $(DEVICE)

ghidorah: all
	python3 load.py --device $(DEVICE) --file coco/ghidorah.raw --loadaddr 0x7C00 --execaddr 0x7C00

colorbar: all
	python3 load.py --device $(DEVICE) --file coco/colorbar.raw --loadaddr 0x2600 --execaddr 0x2600

co: all
	python3 load.py --device $(DEVICE) --file coco/co.raw --loadaddr 0x2600 --execaddr 0x2600

loadromemu: coco/ghidorah.rom
	ostrich2.py --device $(EMUDEVICE) write --address 0xc000 coco/ghidorah.rom
