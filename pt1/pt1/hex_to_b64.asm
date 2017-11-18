global _start
section .data

	b64_table:
		db "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

section .bss
	
	BUFFLEN equ 3072
	Buff resb BUFFLEN

	Conv_Buff resb 3	

section .text
_start:
	
	nop			; for debugging

	call read_buff		; fill buffer 
	xor rcx, rcx		; clear rcx
.conv_loop:
	lea rax, [rcx*3] 	; index from which to read from buff
	shl rax, 1
	mov rbx, rsi		; stor rsi in rbc for manipulating
	sub rbx, rax		; if rbx - rax = 1 then we are at EOF
	cmp rbx, 1		; check to see if we have read entire buff
	jbe write		; if so, write out
	lea rbx, [Buff+rax]	; adress from which to read in buff
	call hex_to_binary	
	lea rax, [rcx*4]	; index from which to right into buff
	lea rbx, [Buff+rax]	; address from which to write into buff
	call binary_to_b64
	inc rcx			; conv next set of vals
	jmp .conv_loop
	nop			; for debugging

; writes rsi bytes from Buff to sdtout and exits
exit:
	mov rax, 1
	mov rdi, 0
	int 0x80

write:
	lea rdx, [rcx * 4]	; char read in rsi
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
	push rcx		; preserve register value
	push rdx		; preserve register value
	xor rax, rax		; zero out rax for usage
	mov rcx, 6		; counter
.get_hex_val:
	dec rcx			; decrement counter
	mov rdi, 2		; for balancing counter into conv_buff later
	cmp byte [rbx+rcx], 4	; if ascii value is 4, we have reached eof
	je .ret			; jump to error if the passed string isn't hex
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
	jnz .cont_store		; if it is odd, dont shift to upper 4 bits
	shl rax, 4		; if it is not, store the hexval in upper 4 bits of byte-space
	add al, [Conv_Buff+rdi]	; retrieve the lower 4 bits and add aswell
.cont_store:
	mov byte [Conv_Buff+rdi], al	; store result in conv_buff
	cmp rcx, 0		; check if we are done
	jnz .get_hex_val	; if not, repeat
.ret:
	pop rdx			; restore rcx
	pop rcx			; restore rcx
	pop rax			; restore rax
	ret			; return

; Converts a 3 byte binary number to a 4 digit base64 number
; Pass number to convert in conv_buff
; Writes base64 number to rbx
binary_to_b64:
	push rcx		; preserve register
	push rax		; preserve register
	xor rax, rax		; clear rax
	mov rcx, [Conv_Buff]	; move binary val to rcx
	mov rax, rcx		; move binary val to rax
	and rax, 0x3f		; mask out all but lower 6 bits
	mov al, [b64_table + rax]
	mov byte [rbx+3], al 	; write b64 value
	mov rax, rcx		; move binary val to rax
	shr rax, 6		; shift rax to lower 6 bits
	and rax, 0x3f	; mask out all but lower 6 bits
	mov al, [b64_table + rax]
	mov byte [rbx+2], al	; write b64 value
	mov rax, rcx		; move binary val to rax
	shr rax, 12		; shift rax to lower 6 bits
	and rax, 0x3f		; mask out all but lower 6 bits
	mov al, [b64_table + rax]
	mov byte [rbx+1], al	; write b64 value
	mov rax, rcx		; move binary val to rax
	shr rax, 18		; shift rax to lower 6 bits
	and rax, 0x3f	; mask out all but lower 6 bits
	mov al, [b64_table + rax]
	mov byte [rbx], al	; write b64 value
	pop rax		; restore register
	pop rcx		; restore register
	ret


error:
	mov rax, 1		; specify sys_exit
	mov rdi, 1		; error
	int 0x80
