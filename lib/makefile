hex_to_binary : hex_to_binary.o
	ld -o hex_to_binary hex_to_binary.o

hex_to_binary.o : hex_to_binary.asm
	nasm -f elf64 -g -F stabs hex_to_binary.asm -l hex_to_binary.lst
