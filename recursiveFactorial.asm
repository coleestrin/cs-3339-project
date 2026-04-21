.data
int:		.word 5
answer:		.word 0

.text
main:		
		#get value to factorialize
		lw $t0, int
		
		beq $t0, $zero, base_case
		
		addi $t1, $zero, 1
		
factorial_func:	#mult fac
		mul $t1, $t1, $t0
		addi $t0, $t0, -1
		beq $t0, $zero, finish_fac
			
		j factorial_func
			
base_case: 	#handle 0 by setting result to 1
		addi $t0, $zero, 1
		
finish_fac:	#store result
		sw $t1, answer
		
		#end program
		nop
		
		