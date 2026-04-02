	.data

finAdd:	.space 10

	.text
main:
	li $t0, 4
	li $t1, 5
	add $t2, $t1, $t0
	sub $t3, $t1, $t0
	mul $t4, $t1, $t0
	
	la $t5, finAdd
	sw $t4, 0($t5)
	
	#exit
	li $v0, 10
	syscall
