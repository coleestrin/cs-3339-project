	.data

finAdd:	.space 10

	.text
main:
	li $t0, 4
	li $t1, 5
	add $t2, $t1, $t0
	sub $t3, $t1, $t0
	mul $t4, $t1, $t0
	
	sw $t4, (finAdd)
	
	#exit
	li $v0, 10
	syscall