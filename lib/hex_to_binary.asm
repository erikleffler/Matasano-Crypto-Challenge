global _start
section .data
section .bss
	
	BUFFLEN equ 1024
	Buff resb BUFFLEN

section .text
_start:
	
	nop			; for debugging

	call read_buff		; fill buffer 
	mov rcx, 0		; put bytes read in rcx for counting
.conv_loop:
	mov rbx, Buff		; adress from which to read in buff
	call hex_to_binary	
	inc rcx			; increment index
	cmp rcx, rsi		; see if we have read entire buff
	je write		; if so, write
	jmp .conv_loop
	nop			; for debugging

; writes rsi bytes from Buff to sdtout and exits
exit:
	mov rax, 1
	mov rdi, 0
	int 0x80

write:
	mov rdx, rsi		; char read in rsi
	shr rdx, 1		; hex to byte ratio is 2:1, therfor divide by two
	mov rax, 4		; specify sys write
	mov rbx, 1		; specify stdout
	mov rcx, Buff		; specify from where to  write from
	int 80H 
	jmp _start		; restart after write

; Read BUFFLEN bytes from stdin and stor in Buff
read_buff:
	mov rax, 3		; specify sys_read
	mov rbx, 0		; specify stdin
	mov rcx, Buff		; store result in Buff
	mov rdx, BUFFLEN	; read BUFFLEN characters
	int 0x80
	mov rsi, rax		; save number of bytes read
	cmp rax, 0		; check return of sys_read for EOF
	je exit			; If EOF is read call exit
	ret

; Conv six hexvalues into a 3 byte binary number and stor in Conv_Buff
; Pass read adress in rbx. Reads from right to left
; stores value in conv_buff
hex_to_binary:
	push rax		; preserve register value
	push rdx		; preserve register value
	xor rax, rax		; zero out rax for usage
.get_hex_val:
	cmp byte [rbx+rcx], 4	; if ascii value is 4, we have reached eof
	je write		; if so, write
	cmp byte [rbx+rcx], 10	; if ascii value is 12, we have reached newline
	je write		; if so, write
	cmp byte [rbx+rcx], 13	; if ascii value is 12, we have reached newline
	je write		; if so, write
	cmp byte [rbx+rcx], 48	; if ascii value is lower than 48 it is not hex
	jb error		; jump to error if the passed string isn't hex
	cmp byte [rbx+rcx], 58	; if ascii value is lower than 58 it is a digit
	jb .digit
	cmp byte [rbx+rcx], 65	; if ascii value is lower -> not hex
	jb error
	cmp byte [rbx+rcx], 71	; if ascii value is lower than 91 it is a uppercaset
	jb .uppercase
	cmp byte [rbx+rcx], 97	; if ascii value is lower -> not hex
	jb error
	cmp byte [rbx+rcx], 103	; if ascii value is lower than 91 it is a lowercaset
	jb .lowercase

.digit:
	mov al, [rbx+rcx]	; store ascii in rax
	sub rax, 48		; turn hex-ascii value in to binary value
	jmp .store		; store the value in conv_buff

.uppercase:
	mov al, [rbx+rcx]	; store ascii in rax
	sub rax, 55		; turn hex-ascii value in to binary value
	jmp .store		; store the value in conv_buff

.lowercase:
	mov al, [rbx+rcx]	; store ascii in rax
	sub rax, 87		; turn hex-ascii value in to binary value
	jmp .store		; store the value in conv_buff

.store:
	mov rdx, rcx		; store rcx in rdx for manipualtion
	shr rdx, 1		; retrieve the correct index to insert into conv_buff
	sub rdi, rdx		; the correct index into conv_buff
	test rcx, 1		; check to see if rcx is even
	jnz .add		; if it is odd, dont shift to upper 4 bits
	shl rax, 4		; if it is not, store the hexval in upper 4 bits of byte-space
	jmp .cont_store
.add:
	add al, [rbx+rdx]	; retrieve the lower 4 bits and add aswell
.cont_store:
	mov byte [rbx+rdx], al	; store result in conv_buff
	pop rdx			; restore rcx
	pop rax			; restore rax
	ret			; return

error:
	mov rax, 1		; specify sys_exit
	mov rdi, 1		; error
	int 0x80
