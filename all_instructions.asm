main:		
		#simulate .data section by simulating start of memory storing data
		#set start of mem
		addi $s0, $zero, 0
		
		addi $t9, $zero, 20
		sw $t9, 0($s0) #integer1 stored in memory at 0
		
		addi $t8, $zero, 4
		sw $t8, 4($s0) #integer2 stored in memory at 4
		
		and $t9, $t9, $zero #resets register $t9
		and $t8, $t8, $zero #resets register $t8


		lw $t1, 0($s0) #get integer1 and store in $t1
		lw $t2, 4($s0) #get integer2 and store in $t2
		add $t0, $t0, $t1 #$t0 is working register
		mul $t0, $t0, $t1
		sub $t0, $t0, $t2
		#checks if last bit is even
		addi $t3, $t3, 1 #sets t3 to 1 to check t4's result in next instruction	
		and $t4, $t0, $t3 #sets t4 to either 0 or 1
		beq $t4, $zero, is_even
		nop
		addi $t0, $t0, 1
		j continue
		nop
is_even:
		srl $t0, $t0, 2 #div by 2^2=4
continue:
		sll $t0, $t0, 4 #mult by 2^4=16
		or $t0, $t0, $t3 #forces t0 to be odd
		
		sw $t0, 8($s0) #stores result in memory at 8 bytes from start
		
		
exit:
		nop

