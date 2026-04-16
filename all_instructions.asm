		.data
		
integer1:	.word 20
integer2:	.word 4
result:		.word 0


		.text
main:		
		lw $t1, integer1
		lw $t2, integer2
		add $t0, $t0, $t1
		mul $t0, $t0, $t1
		div $t0, $t0, $t2
		sub $t0, $t0, $t2
		#checks if last bit is even
		add $t3, $t3, 1 #sets t3 to 1 to check t4's result in next instruction	
		and $t4, $t0, $t3 #sets t4 to either 0 or 1
		beq $t0, $zero, is_even
		nop
		addi $t0, $t0, 1
		j continue
		nop
is_even:
		srl $t0, $t0, 2 #div by 2^2=4
continue:
		sll $t0, $t0, 4 #mult by 2^4=16
		or $t0, $t0, $t3 #forces t0 to be odd
		
		sw $t0, result	
		
		
exit:
		li $v0, 10
		syscall

