hex_to_b64 : hex_to_b64.o
	ld -o hex_to_b64 hex_to_b64.o

hex_to_b64.o : hex_to_b64.asm
	nasm -f elf64 -g -F stabs hex_to_b64.asm -l hex_to_b64.lst
