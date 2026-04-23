main:		
		#simulate .data section by simulating start of memory storing data
		#set start of mem
		addi $s0, $zero, 0 
		addi $t9, $zero, 5
		nop
		nop
		nop
		sw $t9, 0($s0) #int stored in memory at 0
		#answer will be in memory at 4 bytes from start
		
		and $t9, $t9, $zero #resets register $t9
		
		#get value to factorialize
		lw $t0, 0($s0)
		nop
		nop
		nop
		
		beq $t0, $zero, base_case
		nop
		addi $t1, $zero, 1
		nop
		nop
		nop
		
factorial_func:	#mult fac
		# t1 = t1 * t0
		mul $t1, $t1, $t0
		nop
		nop
		nop

		# t2 = 1
		addi $t2, $zero, 1
		nop
		nop
		nop

		# t0 = t0 - t2
		sub $t0, $t0, $t2
		nop
		nop
		nop

		# check if t0 == 0 (now safe to read updated t0)
		beq $t0, $zero, finish_fac
		nop
		j factorial_func
		nop
		
base_case: 	#handle 0 by setting result to 1
		addi $t1, $zero, 1
		nop
		nop
		nop
		
finish_fac:	#store result
		sw $t1, 4($s0) #store answer in memory
		
		#end program
		nop